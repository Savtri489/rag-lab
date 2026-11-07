"""Stage 2 - Chunking: split long text into retrievable pieces."""
import re


def fixed_chunks(text: str, size: int = 60, overlap: int = 15) -> list[str]:
    """Sliding window of `size` words; consecutive chunks share `overlap` words."""
    if not 0 <= overlap < size:
        raise ValueError("overlap must be >= 0 and smaller than size")
    words = text.split()
    step, chunks, i = size - overlap, [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + size]))
        if i + size >= len(words):
            break
        i += step
    return chunks


def sentence_chunks(text: str, max_words: int = 60) -> list[str]:
    """Pack whole sentences into chunks of at most ~max_words words."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current, count = [], [], 0
    for s in sentences:
        n = len(s.split())
        if current and count + n > max_words:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(s)
        count += n
    if current:
        chunks.append(" ".join(current))
    return chunks
