"""
AI Governance Module: Least-Autonomy Enforcement, Risk Classification, and Runtime Cost-Budget Cap.
"""
from fastapi import HTTPException

# --- 1. Risk Classification Justification ---
RISK_CLASSIFICATION = {
    "tier": "Medium Risk",
    "justification": (
        "The Cred Domain Support Agent operates in the Banking & FinTech sector, answering member loan policy queries "
        "and retrieving application statuses. While it does not execute automated fund transfers or make autonomous final lending "
        "decisions (which would constitute High Risk), it interacts directly with operational loan data and financial terms. "
        "Therefore, it is classified as Medium Risk, requiring robust guardrails, PII masking, deterministic verification, "
        "and independent review stages prior to member delivery."
    )
}

# --- 2. Application Layer: Least-Autonomy Enforcement ---
# Least-autonomy rule: Only the designated Lookup Agent may invoke check_loan_application_status.
# The Retrieval Agent and Composer Agent lack execution bindings to this function by architectural design.
ALLOWED_AGENT_FOR_LOOKUP = "Lookup Agent"

def enforce_least_autonomy(agent_role: str, tool_name: str) -> bool:
    if tool_name == "check_loan_application_status" and agent_role != ALLOWED_AGENT_FOR_LOOKUP:
        return False
    return True

# --- 3. Runtime Layer: Per-Request Cost-Budget Cap ---
MAX_ALLOWED_TOKENS = 1500  # Cost budget threshold per request

def enforce_runtime_cost_budget(estimated_tokens: int):
    if estimated_tokens > MAX_ALLOWED_TOKENS:
        raise HTTPException(
            status_code=429,
            detail=f"Runtime Cost-Budget Exceeded: Request requires {estimated_tokens} tokens, exceeding the per-request ceiling of {MAX_ALLOWED_TOKENS}."
        )