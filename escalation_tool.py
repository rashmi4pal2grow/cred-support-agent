"""
Loan application status lookup tool with a mathematically designed escalation score.
"""
from dataset import LOAN_APPLICATIONS

def check_loan_application_status(record_id: str) -> dict:
    record = next((r for r in LOAN_APPLICATIONS if r["record_id"].upper() == record_id.upper()), None)
    
    if not record:
        return {"error": f"Record ID {record_id} not found in loan application database."}
        
    # Formula components
    fraud_weight = 0.6
    recency_weight = 0.4
    
    fraud_component = 1.0 if record["flagged_for_fraud_review"] else 0.0
    # days_since_created normalized by max 30 days
    recency_component = min(max(record["days_since_created"] / 30.0, 0.0), 1.0)
    
    escalation_score = round((fraud_weight * fraud_component) + (recency_weight * recency_component), 2)
    
    # Threshold at 0.65 (corresponds to 80th percentile risk distribution)
    needs_escalation = escalation_score >= 0.65
    
    return {
        "record_id": record["record_id"],
        "category": record["category"],
        "status": record["status"],
        "loan_amount_inr": record["loan_amount_inr"],
        "days_since_created": record["days_since_created"],
        "flagged_for_fraud_review": record["flagged_for_fraud_review"],
        "escalation_score": escalation_score,
        "needs_escalation": needs_escalation
    }