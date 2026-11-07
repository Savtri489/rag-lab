"""Stage 5 - Generation: build the grounded prompt and get an answer."""
import os
import re

SYSTEM = ("Answer ONLY using the context below. Cite sources like [1]. "
          "If the answer is not in the context, say you don't know.")
IDK = "I don't know based on the documents."
STOP = set("a an the is are was were be to of in on at for and or with by from as it this that "
           "you your do does i can how what which when who my me we our if not no any must may will".split())


def build_prompt(question: str, hits) -> str:
    context = "\n\n".join(f"[{i}] (source: {r['source']})\n{r['text']}"
                          for i, (_, r) in enumerate(hits, 1))
    return f"{SYSTEM}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"


def extractive_answer(question: str, hits) -> str:
    """Offline stand-in for an LLM: return the best-matching sentence with a citation."""
    q = set(re.findall(r"\w+", question.lower())) - STOP
    best_overlap, best_sentence, best_idx = 0, None, 0
    for i, (_, r) in enumerate(hits, 1):
        for sent in re.split(r"(?<=[.!?])\s+", r["text"]):
            overlap = len(q & set(re.findall(r"\w+", sent.lower())))
            if overlap > best_overlap:
                best_overlap, best_sentence, best_idx = overlap, sent, i
    return IDK if best_sentence is None else f"{best_sentence} [{best_idx}]"


def generate(question: str, hits) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=os.getenv("RAG_MODEL", "claude-sonnet-5-5"),
            max_tokens=500,
            messages=[{"role": "user", "content": build_prompt(question, hits)}],
        )
        return msg.content[0].text
    return extractive_answer(question, hits)
