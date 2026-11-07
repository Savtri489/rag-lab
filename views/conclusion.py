import streamlit as st

from ui import cards, hero, section

hero("Conclusion", "How it all fits together",
     "From a question typed in a box to an answer with a citation, in six steps you can now explain.")

section("The journey of one question")
cards([
    ("STEP 1", "You ask", "\"Can I carry forward sick leave?\""),
    ("STEP 2", "The question becomes a vector", "The same method that turned the chunks into numbers is applied to your question."),
    ("STEP 3", "Closest chunks win", "Cosine similarity ranks every chunk; the top-k are kept, or the bot refuses if none is close enough."),
    ("STEP 4", "A prompt is built", "Instruction, numbered context and question go together, so the model can cite [1], [2]."),
    ("STEP 5", "The model answers", "It is told to use only the context and to say \"I don't know\" otherwise."),
    ("STEP 6", "You can check it", "The citation points to the exact chunk and source file."),
])

section("What this lab taught")
cards([
    ("LESSON 1", "Chunking matters", "Small fixed chunks can cut a fact in half. Whole sentences kept it together."),
    ("LESSON 2", "Retrieval decides quality", "The model only sees what retrieval gives it. Wrong chunks mean wrong answers."),
    ("LESSON 3", "Guardrails are needed", "A score threshold lets the bot refuse instead of inventing an answer."),
])

section("Honest limitations")
st.markdown(
    '<div class="note">This demo uses TF-IDF, which matches <b>words</b>, not meaning. It can miss a paraphrase '
    '(\"time off after my baby is born\" shares no words with the maternity leave sentence) and can let an '
    'off-topic question through if one word overlaps. Its evaluation set is also small, so a perfect hit rate here '
    'proves the pipeline works, not that it is production-ready.</div>', unsafe_allow_html=True)

section("From classroom to production")
cards([
    ("UPGRADE", "Semantic embeddings", "Models that understand meaning, so paraphrases are found."),
    ("UPGRADE", "A vector database", "FAISS, Chroma or pgvector for millions of chunks."),
    ("UPGRADE", "Reranking and hybrid search", "Combine keyword and semantic scores, then rerank the best few."),
    ("UPGRADE", "A real LLM", "Let a model write fluent answers from the same prompt."),
    ("UPGRADE", "Evaluation", "A larger question set, hit rate, MRR and a faithfulness check."),
    ("UPGRADE", "Security", "Treat retrieved text as untrusted and control who can see which documents."),
])

section("Keep going")
st.page_link("views/demo.py", label="Back to the live demo")
st.page_link("views/home.py", label="Back to the home page")