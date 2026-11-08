"""
Verification script for Part 3: Autogen Review, Governance, and Caching.
"""
from autogen_review import autogen_reviewer
from governance import enforce_least_autonomy, enforce_runtime_cost_budget, RISK_CLASSIFICATION
from cache import response_cache
from fastapi import HTTPException
import time

def run_verifications():
    print("=== TASK 14: Autogen Review Stage Verification ===")
    ctx = "Cred personal loans require income above ₹25,000 and age 21-60."
    
    # Case A: Approved unchanged draft
    valid_draft = "Cred personal loans require applicants to have a monthly income exceeding ₹25,000 and be between 21 and 60 years old."
    verdict_a = autogen_reviewer.review_draft(valid_draft, ctx)
    print(f"Case A (Approval): Approved={verdict_a.approved} | Reason: {verdict_a.reason}")
    assert verdict_a.approved is True
    
    # Case B: Revised draft (catching ungrounded injection)
    injected_draft = "Cred personal loans offer guaranteed 0% interest and unlimited cash advance."
    verdict_b = autogen_reviewer.review_draft(injected_draft, ctx)
    print(f"Case B (Revision): Approved={verdict_b.approved} | Revised Answer: {verdict_b.final_answer} | Reason: {verdict_b.reason}")
    assert verdict_b.approved is False
    
    print("\n=== TASK 15: AI Governance Verification ===")
    print(f"Risk Classification Tier: {RISK_CLASSIFICATION['tier']}")
    print(f"Justification: {RISK_CLASSIFICATION['justification'][:120]}...")
    
    # Least Autonomy test
    allowed = enforce_least_autonomy("Lookup Agent", "check_loan_application_status")
    blocked = enforce_least_autonomy("Composer Agent", "check_loan_application_status")
    print(f"Lookup Agent tool access allowed? {allowed}")
    print(f"Composer Agent tool access blocked? {not blocked}")
    assert allowed is True and blocked is False
    
    # Runtime budget test
    try:
        enforce_runtime_cost_budget(2500) # Oversized request
    except HTTPException as e:
        print(f"Runtime Budget Enforcement successfully caught oversized request: {e.detail}")

    print("\n=== TASK 16: Response Caching Verification ===")
    q = "What are the personal loan eligibility criteria?"
    ans = "Applicants must be aged 21-60 with monthly income > ₹25,000."
    
    # First call (Cache Miss)
    res_miss, t_miss = response_cache.get(q)
    print(f"1st Call Result: {res_miss} | Time: {t_miss:.4f}ms (Cache Miss)")
    response_cache.set(q, ans)
    
    # Second call (Cache Hit)
    res_hit, t_hit = response_cache.get(q)
    print(f"2nd Call Result: {res_hit} | Time: {t_hit:.4f}ms (Cache Hit)")
    print(f"Cache Statistics -> Hits: {response_cache.cache_hits}, Misses: {response_cache.cache_misses}, Total Tool/LLM Calls: {response_cache.call_counter}")
    assert res_hit == ans
    assert response_cache.cache_hits == 1

if __name__ == "__main__":
    run_verifications()