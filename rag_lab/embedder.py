"""Stage 3 - Embedding: turn text into vectors (unit length, so dot product = cosine)."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbedder:
    """Keyword-style vectors. Works offline, needs no model download."""
    name = "tfidf"

    def __init__(self):
        self.vec = TfidfVectorizer(stop_words="english", sublinear_tf=True)

    def fit(self, texts):
        self.vec.fit(texts)
        return self

    def encode(self, texts) -> np.ndarray:
        return self.vec.transform(texts).toarray().astype("float32")  # L2-normalised


class SentenceTransformerEmbedder:
    """Real semantic vectors (understands synonyms). Needs `pip install sentence-transformers`."""
    name = "sentence-transformers"

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model)

    def fit(self, texts):
        return self  # pretrained, nothing to fit

    def encode(self, texts) -> np.ndarray:
        return self.model.encode(list(texts), normalize_embeddings=True).astype("float32")


def get_embedder(kind: str = "tfidf"):
    if kind == "tfidf":
        return TfidfEmbedder()
    if kind in ("st", "sentence-transformers"):
        return SentenceTransformerEmbedder()
    raise ValueError(f"unknown embedder: {kind}")
