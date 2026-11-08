"""
Knowledge Base containing >=12 required topics, each 2-5 sentences.
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb-01",
        "topic": "loan eligibility criteria by loan type",
        "content": "To be eligible for a personal loan at Cred, applicants must be Indian residents aged between 21 and 60 years with a steady monthly income exceeding ₹25,000. Home and business loans require collateral verification, a minimum CIBIL score of 750, and at least 3 years of continuous operational history for business entities. Education loans require admission confirmation to a recognized institution alongside a co-applicant with verifiable income."
    },
    {
        "id": "kb-02",
        "topic": "EMI calculation rules",
        "content": "Equated Monthly Installments (EMIs) are calculated using the standard reducing balance formula incorporating principal amount, annual interest rate, and tenure in months. The formula divides the product of the principal, monthly interest rate, and compounded growth factor by the amortized denominator. Partial prepayments automatically recalculate future EMIs while keeping the loan tenure fixed, unless a tenure reduction is explicitly requested."
    },
    {
        "id": "kb-03",
        "topic": "credit-card fee structure",
        "content": "Cred member credit cards carry zero annual fees for members maintaining an active credit score above 750. Standard transaction processing incurs a 1.5% foreign currency markup fee for international purchases. Late payment fees range from ₹500 to ₹1,300 depending on the outstanding statement balance tier."
    },
    {
        "id": "kb-04",
        "topic": "KYC document requirements",
        "content": "Mandatory Know Your Customer (KYC) documentation includes a government-issued PAN card and Aadhaar card for identity and address verification. Additional requirements include recent salary slips or Form 16 for employed individuals, and audited balance sheets for self-employed applicants. Video KYC verification is mandatory for all high-value loan disbursements exceeding ₹10,00,000."
    },
    {
        "id": "kb-05",
        "topic": "fraud-dispute resolution process",
        "content": "Members can report unauthorized or disputed transactions directly through the Cred app support portal within 30 days of the statement date. Our specialized fraud operations team initiates a temporary hold on the disputed charge while conducting an internal investigation. Resolution and provisional credit reversal are typically completed within 7 to 10 working days."
    },
    {
        "id": "kb-06",
        "topic": "account-closure process",
        "content": "Account closure requests can be initiated via the profile settings menu once all outstanding loan balances, credit card dues, and fees are completely cleared. Members must submit a formal account closure form along with proof of zero balance confirmation. The account is permanently deactivated within 3 to 5 business days following final audit clearance."
    },
    {
        "id": "kb-07",
        "topic": "interest-rate slabs",
        "content": "Interest rates on Cred loans are tiered based on the applicant's risk profile and CIBIL score bracket. Slabs range from a competitive 10.49% per annum for top-tier members with scores above 800, up to 24.00% per annum for standard risk tiers. Rates are fixed for the entire duration of personal and auto loan contracts."
    },
    {
        "id": "kb-08",
        "topic": "prepayment-penalty rules",
        "content": "Cred offers zero prepayment and foreclosure penalties on floating-rate personal and home loans after the completion of twelve successful EMI payments. For fixed-rate loans or closures within the first year, a nominal foreclosure charge of 2% to 4% of the principal outstanding is applicable. Prepayments must be made via verified net banking or UPI channels linked to the primary account."
    },
    {
        "id": "kb-09",
        "topic": "minimum-balance requirements",
        "content": "Members maintaining linked savings accounts or Cred cash wallets must maintain a zero average monthly balance without incurring penalty charges. However, specific premium credit tiers require a maintaining balance of ₹10,000 in associated partner bank accounts to avail exclusive cashback multipliers. Falling below required thresholds temporarily pauses reward accruals."
    },
    {
        "id": "kb-10",
        "topic": "credit-score impact factors",
        "content": "Credit scores are heavily influenced by payment history, credit utilization ratio, length of credit history, and recent hard inquiries. Timely repayment of monthly loan EMIs and credit card bills positively boosts score ratings. Conversely, multiple loan applications within a short window create adverse hard inquiries that lower overall CIBIL standings."
    },
    {
        "id": "kb-11",
        "topic": "joint-account rules",
        "content": "Joint loan applications permit up to two co-applicants whose combined incomes are evaluated to determine maximum eligible loan amounts. Both primary and secondary account holders share equal legal and financial liability for timely repayment obligations. Documentation for both individuals, including separate KYC verification, is mandatory prior to loan sanctioning."
    },
    {
        "id": "kb-12",
        "topic": "NRI-account eligibility",
        "content": "Non-Resident Indians (NRIs) holding valid NRE or NRO bank accounts are eligible to apply for property and personal loans subject to FEMA regulations. Applications require overseas employment contracts, valid work visas, and certified foreign tax identification numbers. Loan repayments must be remitted directly from approved NRE/NRO accounts through official banking channels."
    }
]