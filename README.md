# Cred Domain Support Agent (Banking & FinTech Track)

Completed by: Rashmi Pal / Developer  
**Track:** Banking & FinTech (Cred)  
**Status:** Completed under 100% Deterministic `MOCK_LLM` mode with zero API keys and zero network access.

## Repository Overview
This repository contains the complete production-minded agent architecture for Cred's lending-operations team, answering loan policy questions and looking up application statuses instantly and consistently. It integrates dataset design, dual-strategy RAG retrieval, a multi-agent CrewAI crew, an Autogen review stage, four-layer AI governance, response caching, ELK-style structured logging, input/output guardrails, and a FastAPI production deployment.

## Dataset Design Choices (Part 1, Task 1)
To reproduce this dataset deterministically, use the following configuration in `dataset.py`:
- **Random Seed:** `42`
- **Total Records:** 45 records ($\ge 40$ required)
- **Categories:** Personal Loan (30%), Home Loan (20%), Auto Loan (20%), Education Loan (15%), Business Loan (15%) — *every given category appears $\ge 3$ times.*
- **Statuses:** Submitted (20%), Under Review (25%), Approved (25%), Rejected (15%), Disbursed (15%) — *every status appears $\ge 1$ time.*
- **Loan Amount Range:** ₹50,000 to ₹50,00,000 (INR) — reflecting micro-loans to high-ticket real estate and business loans in India.
- **Fraud Review Percentage:** Exactly 20.0% (satisfying the 10%–30% mandatory band).

## Zero-Network & Telemetry Compliance
Before running the crew or server, telemetry is explicitly disabled to ensure zero outbound network calls:
```bash
export CREWAI_DISABLE_TELEMETRY=true
export OTEL_SDK_DISABLED=true