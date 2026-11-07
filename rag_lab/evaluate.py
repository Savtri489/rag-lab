"""Measure retrieval quality: hit rate@k and MRR over a small labelled question set."""


def evaluate(pipe, cases: list[dict]) -> dict:
    hits_found, reciprocal = 0, 0.0
    for c in cases:
        results = pipe.retrieve(c["question"])
        rank = next((i for i, (_, r) in enumerate(results, 1)
                     if r["source"] == c["expected_source"]
                     and c["must_contain"].lower() in r["text"].lower()), None)
        if rank:
            hits_found += 1
            reciprocal += 1 / rank
    n = len(cases)
    return {"hit_rate": hits_found / n, "mrr": reciprocal / n, "n": n}
