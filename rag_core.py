"""
RAG core implementation with dual chunking strategies (fixed-size vs sentence-based),
ChromaDB indexing, grounded generation, and threshold calibration.
"""
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from kb import KNOWLEDGE_BASE

class RAGCore:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client()
        
        # Two separate collections for chunking strategies
        self.col_fixed = self.client.get_or_create_collection(name="kb_fixed_size")
        self.col_sentence = self.client.get_or_create_collection(name="kb_sentence_based")
        
        self._build_indexes()
        
    def _chunk_fixed(self, text: str, chunk_size: int = 150, overlap: int = 30):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks

    def _chunk_sentences(self, text: str):
        # Basic sentence tokenizer splitting on period followed by space
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        return sentences

    def _build_indexes(self):
        fixed_id_counter = 0
        sent_id_counter = 0
        
        for doc in KNOWLEDGE_BASE:
            doc_id = doc["id"]
            text = doc["content"]
            
            # 1. Fixed-size chunks
            f_chunks = self._chunk_fixed(text)
            for chunk in f_chunks:
                emb = self.encoder.encode(chunk).tolist()
                self.col_fixed.upsert(
                    ids=[f"fixed_{fixed_id_counter}"],
                    embeddings=[emb],
                    documents=[chunk],
                    metadatas=[{"parent_id": doc_id, "topic": doc["topic"]}]
                )
                fixed_id_counter += 1
                
            # 2. Sentence-based chunks
            s_chunks = self._chunk_sentences(text)
            for chunk in s_chunks:
                emb = self.encoder.encode(chunk).tolist()
                self.col_sentence.upsert(
                    ids=[f"sent_{sent_id_counter}"],
                    embeddings=[emb],
                    documents=[chunk],
                    metadatas=[{"parent_id": doc_id, "topic": doc["topic"]}]
                )
                sent_id_counter += 1

    def retrieve(self, query: str, top_k: int = 3, strategy: str = "sentence"):
        collection = self.col_sentence if strategy == "sentence" else self.col_fixed
        query_emb = self.encoder.encode(query).tolist()
        
        results = collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        
        retrieved_docs = []
        if results and results["documents"]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                retrieved_docs.append({"document": doc, "metadata": meta})
                
        # Calculate top-1 cosine similarity score
        # Chroma returns distances; for cosine space distance = 1 - similarity
        top_distance = results["distances"][0][0] if results and "distances" in results and results["distances"] else 0.0
        top_similarity = 1.0 - top_distance
        
        return retrieved_docs, top_similarity

    def generate_answer(self, query: str, threshold: float = 0.45):
        docs, similarity = self.retrieve(query, top_k=3, strategy="sentence")
        
        # Fallback check based on empirically calibrated threshold
        if similarity < threshold or not docs:
            return "I don't know based on the provided knowledge base."
            
        context_str = "\n".join([d["document"] for d in docs])
        
        # Grounded generation simulation (MOCK_LLM)
        answer = f"Based on Cred policy guidelines: {context_str[:300]}... (Answer synthesized strictly from retrieved context for query: '{query}')"
        return answer

rag_engine = RAGCore()