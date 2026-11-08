"""
Autogen Review Stage using RoundRobinGroupChat with Pydantic structured output verdicts.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class YourVerdictModel(BaseModel):
    approved: bool = Field(..., description="True if draft is approved unchanged, False if revision is needed.")
    final_answer: str = Field(..., description="The final approved or revised response text for the member.")
    reason: str = Field(..., description="Justification for approval or specific corrections made.")

class MockAutogenReviewTeam:
    """
    Simulates the Autogen 2-agent Round Robin Group Chat review stage under MOCK_LLM mode.
    Demonstrates both approval (unchanged) and revision (catching ungrounded/injected claims).
    """
    def review_draft(self, draft_answer: str, retrieved_context: str) -> YourVerdictModel:
        # Check for deliberate ungrounded injections or hallucinations
        unsupported_phrases = ["guaranteed 0% interest", "unlimited cash advance", "fake-policy-injection"]
        has_ungrounded_claim = any(phrase in draft_answer.lower() for phrase in unsupported_phrases)
        
        if has_ungrounded_claim:
            # Revision case: catches ungrounded claim and revises draft strictly against retrieved context
            revised_text = f"Based strictly on official Cred policy: {retrieved_context[:250]}..."
            return YourVerdictModel(
                approved=False,
                final_answer=revised_text,
                reason="Policy-Compliance-Reviewer detected ungrounded or unsupported claims in draft. Final-Editor revised the response to match certified knowledge base context."
            )
        else:
            # Approval case: draft is fully grounded and compliant
            return YourVerdictModel(
                approved=True,
                final_answer=draft_answer,
                reason="Draft is fully supported by retrieved context and complies with Cred lending guidelines. Approved unchanged."
            )

autogen_reviewer = MockAutogenReviewTeam()