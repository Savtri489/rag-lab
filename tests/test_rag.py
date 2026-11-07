import json
import os

import pytest

from rag_lab.chunker import fixed_chunks, sentence_chunks
from rag_lab.evaluate import evaluate
from rag_lab.pipeline import RAGPipeline

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def test_fixed_chunks_overlap_and_coverage():
    text = " ".join(f"w{i}" for i in range(100))
    chunks = fixed_chunks(text, size=30, overlap=10)
    assert chunks[0].split()[-10:] == chunks[1].split()[:10]       # overlap shared
    assert chunks[-1].split()[-1] == "w99"                          # nothing lost at the end


def test_fixed_chunks_rejects_bad_overlap():
    with pytest.raises(ValueError):
        fixed_chunks("a b c", size=5, overlap=5)


def test_sentence_chunks_keep_sentences_whole():
    text = "One two three. Four five six. Seven eight nine."
    assert sentence_chunks(text, max_words=6) == ["One two three. Four five six.", "Seven eight nine."]


def make(**kw):
    p = RAGPipeline(**kw)
    p.ingest_folder(DATA)
    return p


def test_answers_are_grounded_and_cited():
    res = make().ask("How long is the password reset link valid?")
    assert "15 minutes" in res["answer"] and "[" in res["answer"]
    assert "Context:" in res["prompt"]


def test_refuses_when_not_in_documents():
    res = make().ask("What is the capital of Mongolia?")
    assert res["answer"] == "I don't know based on the documents."


@pytest.mark.parametrize("strategy,size", [("sentence", 40), ("fixed", 40)])
def test_retrieval_quality(strategy, size):
    cases = json.load(open(os.path.join(DATA, "eval_set.json"), encoding="utf-8"))
    report = evaluate(make(strategy=strategy, size=size, overlap=10), cases)
    assert report["hit_rate"] >= 0.8, report
