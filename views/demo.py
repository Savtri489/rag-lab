import os

import streamlit as st

from ui import esc, get_pipeline, hero

EXAMPLES = [
    "Can I carry forward sick leave?",
    "What is the hotel limit in metro cities?",
    "Which Wi-Fi network should I connect to?",
    "What is the capital of Mongolia?",
]

hero("Live demo", "Ask the documents",
     "Pick a question or type your own. Then explore the answer, the retrieved chunks, the prompt and the chunk map.")

st.session_state.setdefault("question", EXAMPLES[0])
for col, q in zip(st.columns(len(EXAMPLES)), EXAMPLES):
    if col.button(q, use_container_width=True, key=f"ex_{q}"):
        st.session_state.question = q
question = st.text_input("Your question", key="question")

c1, c2, c3, c4 = st.columns(4)
strategy = c1.selectbox("Chunking strategy", ["sentence", "fixed"])
size = c2.slider("Chunk size (words)", 10, 150, 40)
overlap = c3.slider("Overlap (fixed only)", 0, 60, 10, disabled=strategy != "fixed")
k = c4.slider("Top-k chunks", 1, 5, 3)

pipe = get_pipeline(strategy, size, min(overlap, size - 1), k)
records = pipe.store.records
if not question.strip():
    st.info("Type a question to begin.")
    st.stop()

result = pipe.ask(question)
qvec = pipe.embedder.encode([question])[0]
scores = {(r["source"], r["chunk_id"]): s for s, r in pipe.store.search(qvec, len(records))}
top_keys = {(r["source"], r["chunk_id"]) for _, r in result["hits"]}
best = result["hits"][0][0] if result["hits"] else 0.0
refused = result["prompt"] is None

m1, m2, m3 = st.columns(3)
m1.metric("Chunks indexed", len(records))
m2.metric("Best similarity", f"{best:.2f}")
m3.markdown(f'<span class="pill {"no" if refused else "ok"}">{"Refused: not in documents" if refused else "Answered from documents"}</span>',
            unsafe_allow_html=True)

t_answer, t_chunks, t_prompt, t_map = st.tabs(["Answer", "Retrieved chunks", "Prompt", "Chunk map"])

with t_answer:
    (st.warning if refused else st.success)(result["answer"])
    mode = "a real LLM" if os.getenv("ANTHROPIC_API_KEY") else "the offline answerer, which picks the best sentence"
    st.caption(f"Answer written by {mode}. The number in brackets is the chunk it came from.")

with t_chunks:
    for i, (score, r) in enumerate(result["hits"], 1):
        st.markdown(
            f'<div class="hit"><b>[{i}] {esc(r["source"])}</b> <span>chunk {r["chunk_id"] + 1}, similarity {score:.2f}</span>'
            f'<div class="bar"><i style="width:{min(100, round(score * 100))}%"></i></div>{esc(r["text"])}</div>',
            unsafe_allow_html=True)

with t_prompt:
    if refused:
        st.info("The best similarity is below the threshold, so no prompt is sent to a model.")
    else:
        st.code(result["prompt"], language="text")

with t_map:
    st.caption("Each block is a chunk, as wide as its word count. Darker teal means more similar to the question. Amber outline means retrieved.")
    blocks = "".join(
        f'<div class="{"top" if (r["source"], r["chunk_id"]) in top_keys else ""}" '
        f'style="flex:{len(r["text"].split())};background:color-mix(in srgb,#0F7B7D {min(100, round(scores[(r["source"], r["chunk_id"])] * 180))}%,#E3E9F0)" '
        f'title="{esc(r["source"])} chunk {r["chunk_id"] + 1}: {scores[(r["source"], r["chunk_id"])]:.2f}">{n}</div>'
        for n, r in enumerate(records, 1))
    st.markdown(f'<div class="map">{blocks}</div>', unsafe_allow_html=True)
    st.caption("Try: set the strategy to fixed with chunk size 12 and ask the password question. A fact can be cut across two chunks.")