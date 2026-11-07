import streamlit as st

from ui import cards, hero, section

hero("Retrieval-Augmented Generation", "RAG Lab",
     "See how an AI assistant finds the right passage in your documents before it answers. "
     "Change the settings, ask questions, and learn by watching each stage.")

section("Why RAG?")
cards([
    ("THE PROBLEM", "Models have not read your files",
     "A language model has never seen your private documents. Asked about them, it may simply guess."),
    ("THE IDEA", "Look it up first",
     "Find the most relevant passages, put them in the prompt, and tell the model to answer only from them."),
    ("THE RESULT", "Grounded answers",
     "Answers that cite their source, and an honest \"I don't know\" when the documents are silent."),
])

section("The pipeline in six stages")
cards([
    ("01", "Load", "Read the documents (here: three company policy files)."),
    ("02", "Chunk", "Cut long text into small pieces that can be searched."),
    ("03", "Embed", "Turn every chunk into a vector of numbers."),
    ("04", "Retrieve", "Turn the question into a vector and find the closest chunks."),
    ("05", "Build prompt", "Combine instruction, retrieved chunks and the question."),
    ("06", "Generate", "A model writes the answer from the chunks, with citations."),
])

section("Where it is used")
cards([
    ("SUPPORT", "Customer help bots", "Answers drawn from product manuals and FAQs."),
    ("INTERNAL", "HR and IT helpdesks", "Leave, Wi-Fi and expense questions answered from policy."),
    ("RESEARCH", "Policy and legal search", "Find the clause that matters, with a citation."),
])

section("Start exploring")
st.page_link("views/demo.py", label="Open the live demo")
st.page_link("views/conclusion.py", label="Jump to the conclusion")