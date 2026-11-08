"""
In-process session memory implementation using LangChain message history primitives.
"""
from langchain_core.chat_history import InMemoryChatMessageHistory

# Global session store
SESSION_STORE = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = InMemoryChatMessageHistory()
    return SESSION_STORE[session_id]

# Demonstration of Multi-turn vs Fresh Conversation
if __name__ == "__main__":
    sid = "session_alpha"
    history = get_session_history(sid)
    
    # Turn 1
    history.add_user_message("What are the personal loan eligibility criteria?")
    history.add_ai_message("Applicants must be aged 21-60 with a monthly income exceeding ₹25,000.")
    
    # Turn 2
    print("--- Multi-Turn Transcript (Session Alpha) ---")
    for msg in history.messages:
        print(f"{msg.type.upper()}: {msg.content}")
        
    # Fresh Conversation Transcript
    fresh_sid = "session_beta"
    fresh_history = get_session_history(fresh_sid)
    print("\n--- Fresh Conversation Transcript (Session Beta) ---")
    print(f"Message count: {len(fresh_history.messages)} (State correctly absent/reset)")