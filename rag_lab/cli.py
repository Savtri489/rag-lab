"""Command line: python -m rag_lab.cli "How many casual leave days do I get?" """
import argparse
import json
import os

from .evaluate import evaluate
from .pipeline import RAGPipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    p = argparse.ArgumentParser(description="RAG Lab")
    p.add_argument("question", nargs="?")
    p.add_argument("--folder", default=os.path.join(ROOT, "data"))
    p.add_argument("--strategy", choices=["fixed", "sentence"], default="sentence")
    p.add_argument("--size", type=int, default=40)
    p.add_argument("--overlap", type=int, default=10)
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--embedder", default="tfidf")
    p.add_argument("--show-prompt", action="store_true")
    p.add_argument("--eval", action="store_true", help="run data/eval_set.json")
    a = p.parse_args()

    pipe = RAGPipeline(a.strategy, a.size, a.overlap, a.k, embedder=a.embedder)
    n = pipe.ingest_folder(a.folder)
    print(f"Indexed {n} chunks ({a.strategy}, size={a.size}, k={a.k})")

    if a.eval:
        cases = json.load(open(os.path.join(a.folder, "eval_set.json"), encoding="utf-8"))
        print(evaluate(pipe, cases))
    if a.question:
        res = pipe.ask(a.question)
        for i, (score, r) in enumerate(res["hits"], 1):
            print(f"  [{i}] {score:.2f}  {r['source']}#{r['chunk_id']}: {r['text'][:80]}...")
        if a.show_prompt and res["prompt"]:
            print("\n--- PROMPT ---\n" + res["prompt"] + "\n--------------")
        print("\nAnswer:", res["answer"])


if __name__ == "__main__":
    main()
