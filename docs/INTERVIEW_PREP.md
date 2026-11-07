# Interview preparation for the RAG Lab project

## 1. The 30-second pitch
"I built RAG Lab, a 45-minute interactive lesson on RAG. Students change chunking and retrieval settings and see which text reaches the prompt. It includes a browser playground, a tested Python pipeline, an evaluation script with hit rate and MRR, challenges and a quiz. I chose RAG because retrieval quality decides whether the answer is right."

## 2. Concepts you must explain without notes
1. **What is RAG and why use it?** Gives an LLM fresh, private, citeable knowledge at question time; reduces hallucination; no retraining.
2. **RAG versus fine-tuning.** RAG injects facts; fine-tuning changes behaviour or style. Facts change often, so RAG is cheaper to update and can cite.
3. **Chunking.** Small chunks are precise but lose context; large chunks keep context but dilute the match and waste tokens. Overlap protects facts cut at boundaries. Alternatives: sentence, paragraph, recursive, semantic chunking.
4. **Embeddings.** Vectors where similar meaning is nearby. TF-IDF is sparse and word-based; sentence embeddings are dense and capture meaning.
5. **Cosine similarity.** Angle between vectors; with unit vectors it is the dot product. Write it in code: `float(a @ b)`.
6. **Top-k and thresholds.** Larger k raises recall but adds noise and cost; the threshold lets the bot say "I don't know".
7. **Vector databases.** Approximate nearest neighbour indexes (HNSW, IVF) trade a little accuracy for big speed; FAISS, Chroma, pgvector, Pinecone. Mine is brute force, fine for thousands of chunks.
8. **Prompt construction.** Instruction, numbered context, question; ask for citations; order and length matter (context window limits).
9. **Evaluation.** Retrieval: hit rate@k, recall, MRR, nDCG. Generation: faithfulness (is it supported by the context?), answer relevance. Always evaluate retrieval separately from generation.
10. **Improving retrieval.** Better chunking, metadata filters, hybrid (keyword + semantic) search, query rewriting, reranking with a cross-encoder.
11. **Failure modes.** Wrong chunk retrieved, answer split across chunks, outdated documents, prompt injection hidden in documents, the model ignoring context.
12. **Security.** Treat retrieved text as untrusted data; never let it override system instructions; apply access control to documents before retrieval.

## 3. Questions about your project (practise aloud)
- Why TF-IDF as the default? Offline, no downloads, easy to see and explain; the embedder interface lets me swap in sentence-transformers.
- What are its limits? It matches words, not meaning, and my dataset is tiny, so my hit rate says little about production.
- How did you test it? 7 pytest tests (chunk overlap, refusal, grounding, retrieval quality) plus an eval set; I also tested the browser logic with jsdom.
- Hit rate 1.0 on the sample set: is that good? It shows the pipeline works on easy questions; it is not proof of quality. I would grow the eval set and add paraphrased and out-of-scope questions.
- What would you change for production? Persistent vector DB, semantic embeddings, hybrid search, reranking, document updates, monitoring, access control.
- How did you decide the 45-minute structure? Objectives first, then time per activity; I timed myself.
- What did you use AI tools for, and what did you do yourself? Be specific and truthful; you must understand every line.

## 4. Instructional design questions
- How do you simplify a hard concept? Break into stages, one idea per section, concrete example before abstraction, let learners change one variable at a time.
- How do you know learners understood? The challenges, the quiz with explanations, and predictions before experiments.
- Self-learning versus instructor-led? Self: clear instructions and instant feedback. Instructor: demos, pair work, discussion prompts.
- What would you improve after pilot feedback? Track where learners get stuck; shorten or reorder sections.

## 5. Code you may be asked to write live
```python
import numpy as np
def cosine(a, b): return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
def top_k(q, M, k=3): return np.argsort(-(M @ q))[:k]          # M rows are unit vectors
def chunk(words, size, overlap): return [words[i:i+size] for i in range(0, len(words), size-overlap)]
```
Know how to explain `fixed_chunks`, `VectorStore.search` and `RAGPipeline.ask` line by line.

## 6. Seven-day plan
Day 1-2: concepts 1-6. Day 3: concepts 7-12. Day 4: re-read your own code and explain it aloud. Day 5: mock interview using sections 3-4. Day 6: write one upgrade and the before/after numbers. Day 7: rehearse the video and pitch.

## 7. Honest answers beat polished ones
If you do not know something, say how you would find out. Interviewers test understanding of your own project far more than buzzwords.
