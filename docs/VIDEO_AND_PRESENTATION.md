# Video and presentation plan (target: 7 to 8 minutes)

The task lists six questions the video must answer. This script maps one section to each. Speak in your own words; use this as a skeleton.

| Time | Section | Task question it answers | What is on screen |
|---|---|---|---|
| 0:00-0:40 | Hook and why RAG | Why this topic? | One slide: an LLM answering a policy question wrongly, then correctly with RAG |
| 0:40-1:40 | Breaking it down | How did you break the concept down? | The six-stage pipeline slide; say why each stage is its own section |
| 1:40-3:00 | How it works | Underlying logic? | Whiteboard or slide: chunk -> vector -> cosine similarity -> top-k -> prompt. Show 2-3 numbers from the real tool |
| 3:00-5:30 | Live demo of the lab | How do interactive elements support learning? | Open `index.html`. Change chunk size and watch the strip. Run the Password link challenge and make it fail, then fix it. Ask an out-of-scope question to show "I don't know" |
| 5:30-6:30 | Student journey | How would a student use it? | Show the 45-minute table from the README; mention instructor-led and self-learning |
| 6:30-7:30 | Real-world apps and next steps | Relevance to real AI apps? | Support bots, HR helpdesks, legal search; show the Python CLI and the eval numbers; name one limitation and your upgrade |

## Slides (6 is enough)
1. Problem: LLMs do not know your documents and guess.
2. The pipeline in one diagram.
3. Chunking trade-offs (too small loses context, too large adds noise).
4. Embeddings and cosine similarity in plain words.
5. Instructional design: learning objectives, the 45-minute flow, why each interaction exists.
6. Results and real-world use: your measured hit rate and MRR, plus limitations.

## Instructional design points to say out loud
- Learning objectives (3): explain the six stages; predict how chunk size changes retrieval; diagnose a failed retrieval.
- Principle used: learn by manipulation. The student changes one variable and sees the effect immediately.
- The challenges escalate: a warm-up, then two where small fixed chunks cut the fact in half. Failing first is the lesson.
- The knowledge check explains why wrong answers are wrong.

## Recording tips
- Rehearse twice; do one clean take, no editing marathon. Record screen plus voice (OBS, Loom or Zoom).
- Zoom the browser to 125 percent. Close other tabs and notifications.
- Say what you tried and what did not work. Honesty about limits scores better than claiming perfection.
- End by showing the GitHub link and the README.

## Evaluation criteria and your evidence
| Criterion | Your proof |
|---|---|
| Technical accuracy | Tests pass, eval numbers, correct explanation of cosine and chunking |
| Instructional design | Objectives, 45-minute plan, escalating challenges |
| Creativity and interactivity | Chunk strip, live challenges, your own challenge |
| Practical application | CLI, optional LLM mode, your upgrade |
| Communication | Clear script, honest limitations |
