# Build guide: from empty folder to submitted project

Important: the task says plagiarism is not accepted and you must explain every line. So do not just unzip and submit. Type the files yourself in this order, run each one, and make the changes in "Make it yours" below. Budget: about 3 days.

## Day 1: understand and build the core (3-4 hours)
**Step 0. Learn the idea (45 min).** Be able to say in one minute: documents are cut into chunks, chunks become vectors, the question becomes a vector, the closest chunks are pasted into the prompt, and the LLM answers from them.

**Step 1. Set up.**
```bash
mkdir rag-lab && cd rag-lab && git init
python -m venv .venv && source .venv/bin/activate
pip install numpy scikit-learn pytest
mkdir rag_lab data tests docs
```
**Step 2. `rag_lab/chunker.py`.** Two functions: `fixed_chunks` (sliding word window with overlap) and `sentence_chunks` (pack whole sentences). Why: chunk size is the biggest quality lever in RAG. Test: `fixed_chunks("a b c d e f", 4, 2)` should give overlapping pieces. Commit.

**Step 3. `rag_lab/embedder.py`.** Wrap scikit-learn `TfidfVectorizer` (`fit`, `encode`). Output vectors are unit length, so dot product equals cosine similarity. Why: this is the "embedding" stage; later you swap in sentence-transformers behind the same two methods.

**Step 4. `rag_lab/vectorstore.py`.** Store a matrix of vectors plus a list of records. `search` does `vectors @ query_vec`, then `argsort`. Why: this is exactly what a vector database does, minus indexing tricks (HNSW, IVF) that make it fast at millions of vectors.

**Step 5. `rag_lab/generator.py`.** `build_prompt` (instruction + numbered context + question), `extractive_answer` (offline fallback), `generate` (calls an LLM if a key exists). Why: the prompt must tell the model to use only the context, cite, and say "I don't know".

**Step 6. `rag_lab/pipeline.py`.** `RAGPipeline.ingest`, `retrieve`, `ask`. The guardrail: if the best score is under `min_score`, refuse. Why: stops hallucination on out-of-scope questions.

**Step 7. Data.** Put 3 short `.txt` files in `data/`. Write documents from a domain you know (see "Make it yours").

**Step 8. CLI and tests.** `rag_lab/cli.py` plus `tests/test_rag.py`. Run `pytest` and the CLI. Commit.

## Day 2: evaluation and the interactive lesson (4-5 hours)
**Step 9. `rag_lab/evaluate.py` and `data/eval_set.json`.** Write 6-10 questions with the expected source and a phrase that must appear in the retrieved chunk. Report hit rate and MRR. Run `--eval` with different chunk sizes and write down the numbers; these go in your video.

**Step 10. `index.html`.** One file, no libraries. Build in this order: (a) text area + chunking, (b) TF-IDF in JavaScript, (c) chunk strip coloured by similarity, (d) retrieved list with highlighted words, (e) prompt preview and answer, (f) challenges, (g) quiz. Keep the JavaScript logic identical to the Python so you can say "same algorithm, two languages".

**Step 11. Test the lesson yourself.** Run it as a student would with a stopwatch. It must fit in 45 minutes. Cut anything that does not teach.

## Day 3: upgrades, polish, ship (3-4 hours)
**Step 12. One upgrade of your own** (pick one, it makes the project yours):
1. Real semantic embeddings: `pip install sentence-transformers`, run with `--embedder st`, compare hit rate with TF-IDF on paraphrased questions.
2. PDF loading with `pypdf` and metadata (page numbers in citations).
3. Hybrid search: combine TF-IDF score and embedding score.
4. Real LLM answers with a key, plus a faithfulness check (does every claim appear in the context?).
5. Swap the store for Chroma or FAISS and explain the trade-offs.

**Step 13. Ship.** Create a public GitHub repo, push, add a `.gitignore` (`.venv`, `__pycache__`), keep `README.md` at the root. Enable GitHub Pages (Settings, Pages, branch `main`, folder `/root`) so `index.html` has a live link. Also build a ZIP: `zip -r rag-lab.zip rag-lab -x "*/.venv/*" "*/__pycache__/*"`. Test the ZIP on a clean folder.

**Step 14. Record the video** using `VIDEO_AND_PRESENTATION.md`. The form can be submitted only once, so check every link while logged out.

## Make it yours (do at least three)
- Replace Nimbus Labs with a domain you know (your college handbook, a hostel policy, CDS exam FAQs).
- Write your own eval questions, including 2 that the system should refuse.
- Add one challenge to `index.html` that you invented.
- Add the upgrade from Step 12 and report measured before/after numbers.
- Write the "What I learned / what failed" section in the README.

## Experiment to run before the video
Ask a question that shares no words with the document (for example, "time off for a newborn" against the paternity leave sentence) with TF-IDF, then with `--embedder st`. Record what you observe. This is your honest demonstration of keyword versus semantic search; report whatever you actually see.
