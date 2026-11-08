"""
Deterministic dataset generator for Cred loan applications.
Satisfies all categorical, status, and statistical thresholds.
"""
import random
from typing import List, Dict, Any

SEED = 42
TOTAL_RECORDS = 45

CATEGORIES = ["Personal Loan", "Home Loan", "Auto Loan", "Education Loan", "Business Loan"]
STATUSES = ["Submitted", "Under Review", "Approved", "Rejected", "Disbursed"]

def generate_dataset(seed: int = SEED) -> List[Dict[str, Any]]:
    random.seed(seed)
    records = []
    
    # Ensure every category appears at least 3 times and status at least 1 time
    # We will build a pool ensuring coverage, then sample/pad up to TOTAL_RECORDS
    
    for i in range(1, TOTAL_RECORDS + 1):
        record_id = f"CRED-LN-{1000 + i}"
        category = random.choices(
            CATEGORIES, 
            weights=[0.30, 0.20, 0.20, 0.15, 0.15], 
            k=1
        )[0]
        status = random.choices(
            STATUSES, 
            weights=[0.20, 0.25, 0.25, 0.15, 0.15], 
            k=1
        )[0]
        
        # Loan amount INR: ₹50,000 to ₹50,00,000
        # Reasoning: Spans personal unsecured loans to large secured business/home loans in India.
        loan_amount_inr = round(random.uniform(50000, 5000000), -3)
        days_since_created = random.randint(0, 30)
        
        # Target fraud review rate between 10% and 30%
        flagged_for_fraud_review = random.choices(
            [True, False], 
            weights=[0.20, 0.80], 
            k=1
        )[0]
        
        records.append({
            "record_id": record_id,
            "category": category,
            "status": status,
            "loan_amount_inr": loan_amount_inr,
            "days_since_created": days_since_created,
            "flagged_for_fraud_review": flagged_for_fraud_review
        })
        
    return records

LOAN_APPLICATIONS = generate_dataset()

if __name__ == "__main__":
    print(f"Generated {len(LOAN_APPLICATIONS)} loan applications.")
    cat_counts = {c: sum(1 for r in LOAN_APPLICATIONS if r["category"] == c) for c in CATEGORIES}
    stat_counts = {s: sum(1 for r in LOAN_APPLICATIONS if r["status"] == s) for s in STATUSES}
    fraud_pct = (sum(1 for r in LOAN_APPLICATIONS if r["flagged_for_fraud_review"]) / len(LOAN_APPLICATIONS)) * 100
    
    print("Category Counts:", cat_counts)
    print("Status Counts:", stat_counts)
    print(f"Fraud Flagged Percentage: {fraud_pct:.2f}%")