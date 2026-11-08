"""
In-memory response cache implementation for Cred Domain Support Agent.
Keyed by normalized query text with hit/miss telemetry and execution timing.
"""
import time
from typing import Dict, Tuple, Optional

class ResponseCache:
    def __init__(self):
        self.store: Dict[str, str] = {}
        self.call_counter: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0

    def normalize_query(self, query: str) -> str:
        return query.strip().lower()

    def get(self, query: str) -> Tuple[Optional[str], float]:
        norm_key = self.normalize_query(query)
        start_time = time.time()
        
        if norm_key in self.store:
            self.cache_hits += 1
            duration = (time.time() - start_time) * 1000
            return self.store[norm_key], duration
        
        self.cache_misses += 1
        return None, (time.time() - start_time) * 1000

    def set(self, query: str, response: str):
        norm_key = self.normalize_query(query)
        self.store[norm_key] = response
        self.call_counter += 1

# Instantiate the global response cache object imported directly by main.py
response_cache = ResponseCache()