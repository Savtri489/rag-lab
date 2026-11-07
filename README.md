# RAG Lab: a 45-minute interactive lesson on Retrieval-Augmented Generation

Students learn how a RAG pipeline works by changing the settings and watching the retrieval change.

## What is inside
| Part | What it is | How to open |
|---|---|---|
| `index.html` | Interactive lesson and playground (no install, no internet) | Double-click the file |
| `rag_lab/` | The same pipeline as real Python code | `python -m rag_lab.cli "your question"` |
| `app.py` | Streamlit live demo of the Python pipeline | `streamlit run app.py` |
| `tests/` | 7 automated tests | `pytest` |
| `docs/` | Build guide, video and presentation plan, interview prep | Read in order |

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                                  # expect: 7 passed
python -m rag_lab.cli "Can I carry forward sick leave?" --show-prompt
python -m rag_lab.cli --eval --strategy fixed --size 20 # compare chunking strategies
```
Optional: `pip install anthropic` and set `ANTHROPIC_API_KEY` to let a real LLM write the answers from the same prompt. Optional: `pip install sentence-transformers` and pass `--embedder st` for real semantic embeddings.

## The pipeline
`Load -> Chunk (chunker.py) -> Embed (embedder.py) -> Store (vectorstore.py) -> Retrieve (pipeline.py) -> Prompt + Generate (generator.py) -> Evaluate (evaluate.py)`

## 45-minute lesson plan
| Min | Activity |
|---|---|
| 0-5 | Read "What is RAG?" and the six stages |
| 5-20 | Explore: change chunk strategy, size, overlap and k; watch the chunk strip and the prompt change |
| 20-35 | Three challenges (warm-up, then two where small fixed chunks cut the fact in half) |
| 35-40 | Knowledge check (3 questions with explanations) |
| 40-45 | Read the Python code, run the CLI, discuss real-world use |

Instructor-led: demo one stage per 3 minutes, then let pairs attempt the challenges. Self-learning: follow the table above.

## Real-world use
Customer-support bots, HR/IT helpdesks, legal and policy search, internal knowledge assistants, documentation Q&A.

## Honest limits
- The default embedder is TF-IDF: it matches words, not meaning. Use `--embedder st` to see semantic search.
- The browser demo answers by picking the best sentence; the Python version can call a real LLM.
- The vector store is in memory by design (for teaching). Production systems use FAISS, Chroma, pgvector or Pinecone.
