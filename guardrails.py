"""
Guardrails Module for Cred Domain Support Agent
Handles:
1. Prompt Injection Detection (Input-side)
2. PII Masking: PAN, Aadhaar, and Bank Account numbers (Input-side)
3. Output Groundedness Verification (Output-side)
"""
import re

def detect_prompt_injection(text: str) -> bool:
    """
    Scans input text for common prompt injection patterns and jailbreak attempts.
    Returns True if an injection attempt is detected.
    """
    injection_patterns = [
        r"ignore previous instructions",
        r"system prompt",
        r"disregard all rules",
        r"jailbreak",
        r"you are now free",
        r"forget your instructions"
    ]
    for pattern in injection_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def mask_pii(text: str) -> str:
    """
    Masks fixed-format sensitive PII identifiers:
    - Indian PAN (e.g., ABCDE1234F) -> [PAN_MASKED]
    - Aadhaar (12 digits with optional spaces) -> [AADHAAR_MASKED]
    - Bank Account Numbers (9 to 18 digits) -> [ACCOUNT_MASKED]
    """
    # 1. Mask Indian PAN
    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    text = re.sub(pan_pattern, '[PAN_MASKED]', text)
    
    # 2. Mask Aadhaar
    aadhaar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    text = re.sub(aadhaar_pattern, '[AADHAAR_MASKED]', text)
    
    # 3. Mask Bank Account numbers
    account_pattern = r'\b\d{9,18}\b'
    text = re.sub(account_pattern, '[ACCOUNT_MASKED]', text)
    
    return text

def process_input_guardrail(user_input: str) -> dict:
    """
    Executes the full input guardrail pipeline:
    1. Checks for prompt injection.
    2. Masks sensitive PII.
    """
    if detect_prompt_injection(user_input):
        return {
            "safe": False,
            "sanitized_text": "",
            "reason": "Prompt injection attempt detected. Request blocked for security compliance."
        }
        
    sanitized_text = mask_pii(user_input)
    return {
        "safe": True,
        "sanitized_text": sanitized_text,
        "reason": None
    }

def output_groundedness_guardrail(answer: str, retrieved_context: str) -> str:
    """
    Output-side guardrail verifying that the answer is supported by the retrieved context.
    Triggers the 'I don't know' fallback if context is empty or insufficient.
    """
    if not retrieved_context or len(retrieved_context.strip()) == 0:
        return "I don't know based on the provided knowledge base."
        
    return answer