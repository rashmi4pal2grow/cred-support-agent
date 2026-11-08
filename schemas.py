"""
Pydantic schema enforcing structured outputs for all crew support responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class SupportResponseSchema(BaseModel):
    response_status: str = Field(..., description="Status of the response: SUCCESS, ESCALATED, or FALLBACK")
    primary_answer: str = Field(..., description="Synthesized answer text grounded in policy or record lookup")
    referenced_topics: List[str] = Field(default=[], description="Knowledge base topics or record IDs referenced")
    escalation_required: bool = Field(..., description="Whether the request requires human operations intervention")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence metric based on retrieval similarity")