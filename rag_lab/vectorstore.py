"""Stage 3b - A tiny in-memory vector store (the idea behind FAISS / Chroma / Pinecone)."""
import numpy as np


class VectorStore:
    def __init__(self):
        self.vectors = None
        self.records: list[dict] = []

    def add(self, vectors: np.ndarray, records: list[dict]) -> None:
        self.vectors = vectors if self.vectors is None else np.vstack([self.vectors, vectors])
        self.records += records

    def search(self, query_vec: np.ndarray, k: int = 3) -> list[tuple[float, dict]]:
        if self.vectors is None:
            return []
        scores = self.vectors @ query_vec  # cosine similarity: vectors are unit length
        top = np.argsort(-scores)[:k]
        return [(float(scores[i]), self.records[i]) for i in top]
