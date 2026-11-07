# Setup, platform choice and live-demo deployment

## 1. Which platform: VS Code or Colab?
Use **VS Code** as your main workspace. Use **Colab** only as an optional extra.

| | VS Code (local) | Google Colab |
|---|---|---|
| Multi-file project with folders, tests, git | Yes, built for it | Awkward: one notebook, files vanish when the session ends |
| Needs a GPU | No, this project runs on any laptop CPU | Not needed either |
| Good for | Building the package, running pytest, pushing to GitHub | A quick notebook demo, trying sentence-transformers without installing |
| Live demo link | Deploy from GitHub (section 4) | Not suitable: sessions are temporary |

A GitHub repo is the submission format the task asks for, and a repo is a folder of files, so VS Code is the natural fit. This project needs no model training; "building the model" here means building the retrieval pipeline.

## 2. Final folder structure
```
rag-lab/
├── app.py                  # Streamlit live demo of the Python pipeline
├── index.html              # static interactive lesson (works with no server)
├── requirements.txt
├── README.md
├── .gitignore
├── rag_lab/                # the pipeline package
│   ├── __init__.py
│   ├── chunker.py          # stage 2: chunking
│   ├── embedder.py         # stage 3: vectors (TF-IDF or sentence-transformers)
│   ├── vectorstore.py      # stage 3b: similarity search
│   ├── generator.py        # stage 5: prompt + answer
│   ├── pipeline.py         # glues all stages together
│   ├── evaluate.py         # hit rate and MRR
│   └── cli.py              # command line entry point
├── data/
│   ├── hr_leave_policy.txt
│   ├── it_support.txt
│   ├── expense_policy.txt
│   └── eval_set.json
├── tests/
│   └── test_rag.py
└── docs/
    ├── BUILD_GUIDE.md
    ├── SETUP_AND_DEPLOY.md
    ├── VIDEO_AND_PRESENTATION.md
    └── INTERVIEW_PREP.md
```

## 3. Step-by-step in VS Code
**Step 1. Install tools (once).** Python 3.10 or newer (python.org; on Windows tick "Add to PATH"), VS Code, Git, and the VS Code extensions "Python" and "Pylance". Create a free GitHub account.

**Step 2. Create the project.** In a terminal:
```bash
mkdir rag-lab && cd rag-lab
code .                      # opens VS Code in this folder
git init
```
**Step 3. Virtual environment.** In the VS Code terminal:
```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install numpy scikit-learn pytest streamlit
```
Then press Ctrl+Shift+P, choose "Python: Select Interpreter", and pick the one inside `.venv`.

**Step 4. Create folders and files** exactly as in the tree above. Write them in this order, running a small check after each one: `chunker.py`, `embedder.py`, `vectorstore.py`, `generator.py`, `pipeline.py`, `cli.py`, then `data/`, then `tests/`.

**Step 5. Run it.**
```bash
python -m pytest -q                                   # all tests pass
python -m rag_lab.cli "Can I carry forward sick leave?" --show-prompt
python -m rag_lab.cli --eval                          # hit rate and MRR
streamlit run app.py                                  # opens http://localhost:8501
```
Open `index.html` by double-clicking it (or use the "Live Server" extension).

**Step 6. Commit often.**
```bash
git add . && git commit -m "Add chunker and tests"
```
**Step 7. Build the lesson page and evaluate** following `BUILD_GUIDE.md` (Day 2), then add your own upgrade (Day 3).

**Step 8. Optional Colab notebook.** In Colab, run `!git clone <your-repo-url>`, `%cd rag-lab`, `!pip install -r requirements.txt`, then call `RAGPipeline` in a cell. Useful for trying `sentence-transformers`. Commit the notebook to `notebooks/` if you make one.

## 4. Deploying a live demo
You have two things to host, and they deploy differently.

### A. The lesson page (`index.html`): GitHub Pages (recommended, free)
It is one static file with no server, so nothing can break.
1. Push the repo to GitHub (public).
2. Repo, Settings, Pages, "Deploy from a branch", branch `main`, folder `/ (root)`, Save.
3. After a minute it is live at `https://<your-username>.github.io/<repo-name>/`.
Alternatives: Netlify or Vercel (drag the folder in or connect the repo).

### B. The Python pipeline (`app.py`): Streamlit Community Cloud (recommended)
1. Repo is public on GitHub, with `app.py` and `requirements.txt` in the root, and all changes pushed.
2. Go to share.streamlit.io, sign in with GitHub, click "New app".
3. Choose the repo, branch `main`, main file `app.py`, and Deploy. It installs `requirements.txt` and gives you a `streamlit.app` link.
4. Check the live link while logged out before you submit.

Things to know (limits can change, so check the current page):
- The free tier is for public apps and has limited memory, and idle apps may go to sleep. Open the link a few minutes before your video or interview so it is awake.
- Keep the default TF-IDF embedder for the hosted demo. Downloading sentence-transformers models makes the build heavy and risks hitting free-tier limits.
- If you add an LLM key, put it in the app's Secrets settings (and read it with `st.secrets` or an environment variable). Never commit keys to GitHub.

Other options: Hugging Face Spaces (free hosting for Streamlit, Gradio or Docker apps), Render, Railway, Fly.io, or Google Cloud Run with a Dockerfile. They need more setup than the two above, so use them only if you want the practice.

### What to submit
Put both links in your README: the GitHub Pages lesson link and the Streamlit link, plus the repo itself (or the ZIP). The ZIP command is in `BUILD_GUIDE.md`, Step 13.

## 5. Common problems
| Problem | Fix |
|---|---|
| `ModuleNotFoundError: rag_lab` | Run commands from the project root, using `python -m ...` |
| `streamlit: command not found` | Activate `.venv`, then `pip install streamlit` |
| Streamlit Cloud build fails | A package is missing from `requirements.txt`; add it, push, reboot the app |
| GitHub Pages shows 404 | Wait a minute, check the branch and folder in Settings, Pages, and that the file is named `index.html` |
| Hosted app is slow on first open | It was asleep; wait for it to wake, then reload |
