"""
CrewAI Multi-Agent Crew implementation with Retrieval, Lookup, and Composer agents.
"""
import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew
from crewai.llms.base_llm import BaseLLM
from rag_core import rag_engine
from escalation_tool import check_loan_application_status

class MockCrewAIModel(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def call(self, messages, tools=None, callbacks=None):
        prompt = " ".join([m.get("content", "") for m in messages]) if isinstance(messages, list) else str(messages)
        
        # Prevent ReAct system-prompt template trap ("Observation: the result of the action")
        if "Observation: the result of the action" in prompt:
            prompt = prompt.replace("Observation: the result of the action", "")
            
        if "CRED-LN-" in prompt:
            # Extract record id and invoke lookup tool
            import re
            match = re.search(r'CRED-LN-\d+', prompt)
            if match:
                res = check_loan_application_status(match.group(0))
                return f"Tool Execution Result (Lookup): {res}"
        
        # Default RAG policy lookup
        docs, _ = rag_engine.retrieve(prompt, top_k=2, strategy="sentence")
        context = " ".join([d["document"] for d in docs])
        return f"Tool Execution Result (RAG): {context}"

# Define Agents
retrieval_agent = Agent(
    role='Knowledge Base Retrieval Specialist',
    goal='Retrieve exact policy guidelines from the Cred knowledge base collections.',
    backstory='Expert in searching vector databases and extracting precise financial regulations.',
    verbose=False,
    llm=MockCrewAIModel()
)

lookup_agent = Agent(
    role='Loan Application Operations Analyst',
    goal='Inspect specific loan records and calculate operational risk scores.',
    backstory='Specialist in lending operations, fraud review flags, and application status tracking.',
    verbose=False,
    llm=MockCrewAIModel()
)

composer_agent = Agent(
    role='Response Composer',
    goal='Synthesize retrieval and lookup outputs into a unified, professional member response.',
    backstory='Senior customer success lead at Cred delivering clear, empathetic, and compliant support.',
    verbose=False,
    llm=MockCrewAIModel()
)