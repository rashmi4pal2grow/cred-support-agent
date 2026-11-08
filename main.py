"""
Unified FastAPI Backend for Cred Domain Support Agent
Includes:
- FastAPI HTTP Endpoints (/ask, /add-document)
- WebSocket Real-Time Chat with Disconnect Resilience (/ws/chat)
- ELK-Style Structured JSON-Lines Logging with PII Masking
- Unified Guardrails (Prompt Injection + PII Masking + Groundedness)
- Autogen Review Stage with Pydantic Verdicts
- AI Governance Checks (Least-Autonomy & Runtime Cost-Budget Cap)
- In-Memory Response Caching
"""
import os
import time
import json
import uuid
import logging
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel, Field

# Zero-network compliance for crew & LLM components
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from guardrails import process_input_guardrail, output_groundedness_guardrail, mask_pii
from rag_core import rag_engine
from dataset import LOAN_APPLICATIONS
from escalation_tool import check_loan_application_status
from agents import review_team
from autogen_review import autogen_reviewer
from governance import enforce_least_autonomy, enforce_runtime_cost_budget, RISK_CLASSIFICATION
from cache import response_cache

# Configure structured ELK-style JSON logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("cred_support_elk")

app = FastAPI(title="Cred Domain Support Agent Production API", version="3.0.0")

# --- Pydantic Request/Response Models ---
class AskRequest(BaseModel):
    query: str = Field(..., description="User support question or application lookup query")
    session_id: str = Field(default="default_session", description="Conversation session identifier")

class AskResponse(BaseModel):
    trace_id: str
    session_id: str
    sanitized_query: str
    response: str
    escalation_required: bool
    review_status: str
    cached: bool

class DocumentRequest(BaseModel):
    topic: str
    content: str

# --- ELK-Style Structured Logger with PII Masking ---
def log_structured_request(trace_id: str, endpoint: str, raw_query: str, duration_ms: float, status_code: int):
    masked_query = mask_pii(raw_query)
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "trace_id": trace_id,
        "endpoint": endpoint,
        "query_masked": masked_query,
        "duration_ms": round(duration_ms, 2),
        "status_code": status_code,
        "risk_tier": RISK_CLASSIFICATION["tier"]
    }
    logger.info(json.dumps(log_entry))

# --- FastAPI Endpoints ---
@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(payload: AskRequest):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    # 1. Input Guardrail (Prompt Injection + PII Masking)
    guard_res = process_input_guardrail(payload.query)
    if not guard_res["safe"]:
        duration = (time.time() - start_time) * 1000
        log_structured_request(trace_id, "POST /ask", payload.query, duration, 400)
        raise HTTPException(status_code=400, detail=guard_res["reason"])
        
    safe_query = guard_res["sanitized_text"]
    
    # 2. Runtime Governance: Cost-Budget Enforcement
    estimated_tokens = len(safe_query.split()) * 15 + 200
    enforce_runtime_cost_budget(estimated_tokens)
    
    # 3. Response Caching Layer Check
    cached_response, cache_duration = response_cache.get(safe_query)
    if cached_response:
        duration = (time.time() - start_time) * 1000
        log_structured_request(trace_id, "POST /ask (Cache Hit)", payload.query, duration, 200)
        return AskResponse(
            trace_id=trace_id,
            session_id=payload.session_id,
            sanitized_query=safe_query,
            response=cached_response,
            escalation_required=False,
            review_status="Cached Approval",
            cached=True
        )
        
    # 4. Core Logic: RAG vs Lookup (Least Autonomy Check for Lookup Tool)
    escalate = False
    if "status" in safe_query.lower() or "CRED-LN-" in safe_query:
        # Enforce least autonomy: Verify tool access rights
        if not enforce_least_autonomy("Lookup Agent", "check_loan_application_status"):
            raise HTTPException(status_code=403, detail="Governance Violation: Unauthorized agent tool access.")
            
        import re
        match = re.search(r'CRED-LN-\d+', safe_query)
        if match:
            res = check_loan_application_status(match.group(0))
            raw_answer = f"Loan Record {res.get('record_id')}: Status is {res.get('status')}, Category is {res.get('category')}, Escalation Score is {res.get('escalation_score')}."
            escalate = res.get("needs_escalation", False)
        else:
            sample = LOAN_APPLICATIONS[0]
            raw_answer = f"Sample Application {sample['record_id']} status is {sample['status']}."
        context_str = "Loan application database record retrieved."
    else:
        docs, _ = rag_engine.retrieve(safe_query, top_k=3, strategy="sentence")
        context_str = " ".join([d["document"] for d in docs])
        raw_answer = rag_engine.generate_answer(safe_query)
        
    # 5. Output Groundedness Guardrail
    grounded_answer = output_groundedness_guardrail(raw_answer, context_str)
    
    # 6. Autogen Review Stage (Pydantic Structured Verdicts)
    verdict = autogen_reviewer.review_draft(grounded_answer, context_str)
    final_output = verdict.final_answer
    
    # 7. Store in Cache
    response_cache.set(safe_query, final_output)
    
    duration = (time.time() - start_time) * 1000
    log_structured_request(trace_id, "POST /ask", payload.query, duration, 200)
    
    return AskResponse(
        trace_id=trace_id,
        session_id=payload.session_id,
        sanitized_query=safe_query,
        response=final_output,
        escalation_required=escalate,
        review_status="Approved" if verdict.approved else "Revised",
        cached=False
    )

@app.post("/add-document")
async def add_document(payload: DocumentRequest):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    doc_id = f"kb-dyn-{int(time.time())}"
    emb = rag_engine.encoder.encode(payload.content).tolist()
    rag_engine.col_sentence.upsert(
        ids=[doc_id],
        embeddings=[emb],
        documents=[payload.content],
        metadatas=[{"parent_id": doc_id, "topic": payload.topic}]
    )
    
    duration = (time.time() - start_time) * 1000
    log_structured_request(trace_id, "POST /add-document", f"Topic: {payload.topic}", duration, 200)
    return {"status": "success", "document_id": doc_id, "trace_id": trace_id}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())[:8]
    try:
        while True:
            data = await websocket.receive_text()
            guard_res = process_input_guardrail(data)
            if not guard_res["safe"]:
                await websocket.send_json({"error": guard_res["reason"]})
                continue
                
            safe_text = guard_res["sanitized_text"]
            
            # Check cache in websocket loop
            cached, _ = response_cache.get(safe_text)
            if cached:
                answer = cached
            else:
                raw_ans = rag_engine.generate_answer(safe_text)
                verdict = autogen_reviewer.review_draft(raw_ans, "Retrieved context for chat query.")
                answer = verdict.final_answer
                response_cache.set(safe_text, answer)
                
            await websocket.send_json({
                "client_id": client_id,
                "echo_query": safe_text,
                "response": answer
            })
    except WebSocketDisconnect:
        logger.info(json.dumps({
            "event": "websocket_disconnect",
            "client_id": client_id,
            "message": "Client disconnected gracefully. Server worker remains active."
        }))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "MOCK_LLM",
        "telemetry": "disabled",
        "risk_tier": RISK_CLASSIFICATION["tier"],
        "cache_stats": {
            "hits": response_cache.cache_hits,
            "misses": response_cache.cache_misses
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)