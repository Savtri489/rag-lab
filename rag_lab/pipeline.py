"""The whole RAG pipeline in one class: ingest -> chunk -> embed -> store -> retrieve -> generate."""
import glob
import os

from .chunker import fixed_chunks, sentence_chunks
from .embedder import get_embedder
from .generator import IDK, build_prompt, generate
from .vectorstore import VectorStore


class RAGPipeline:
    def __init__(self, strategy="sentence", size=40, overlap=10, k=3,
                 min_score=0.08, embedder="tfidf"):
        self.strategy, self.size, self.overlap = strategy, size, overlap
        self.k, self.min_score = k, min_score
        self.embedder = get_embedder(embedder)
        self.store = VectorStore()

    def ingest_folder(self, folder: str) -> int:
        paths = sorted(glob.glob(os.path.join(folder, "*.txt")))
        docs = {os.path.basename(p): open(p, encoding="utf-8").read() for p in paths}
        return self.ingest(docs)

    def ingest(self, docs: dict) -> int:
        records = []
        for source, text in docs.items():
            if self.strategy == "fixed":
                pieces = fixed_chunks(text, self.size, self.overlap)
            else:
                pieces = sentence_chunks(text, self.size)
            records += [{"source": source, "chunk_id": i, "text": t} for i, t in enumerate(pieces)]
        texts = [r["text"] for r in records]
        self.embedder.fit(texts)
        self.store = VectorStore()
        self.store.add(self.embedder.encode(texts), records)
        return len(records)

    def retrieve(self, question: str):
        return self.store.search(self.embedder.encode([question])[0], self.k)

    def ask(self, question: str) -> dict:
        hits = self.retrieve(question)
        if not hits or hits[0][0] < self.min_score:  # guardrail: refuse instead of hallucinating
            return {"answer": IDK, "hits": hits, "prompt": None}
        return {"answer": generate(question, hits), "hits": hits,
                "prompt": build_prompt(question, hits)}
