# ArcLight Copilot

*Illuminating research with agentic AI.*  
**ArcLight Copilot** is a demo-ready, portfolio-grade **agentic research assistant** built with **LangChain** and **Azure OpenAI**, featuring planning, tool use (web/RAG), reflection, and a clean **Streamlit** UI.

> Why this repo? Most demos are chat wrappers. ArcLight **plans tasks, uses tools, cites sources, and self-checks answers**—showcasing real agent patterns and Azure integration.

---

## ✨ Highlights

- **Agentic flow**: Planner → Researcher (RAG/tool use) → Reviewer (reflection) → Final Answer
- **Azure-first**: Azure OpenAI (LLM & embeddings), optional Azure AI Search for RAG
- **Streamlit UI**: one-file run, live step log, exportable run trace
- **Quality**: tests, CI (ruff/black/pytest), Dockerfile, DevContainer
- **Safe defaults**: Runs in a *demo mode* without API keys; full features light up when env vars are set

---

## 🧱 Architecture (at a glance)

```
User
 └─ Streamlit UI
     └─ ArcLight Orchestrator
         ├─ Planner Agent (LangChain Tools Agent)
         ├─ Researcher (RAG chain + tools)
         ├─ Reviewer (critique & retry)
         └─ Finalizer (answer + citations + action log)
Tools:
  - Web Search (stub or Tavily/SerpAPI)
  - Azure AI Search (optional)
  - GitHub Issues (stub)
  - Python Sandbox (restricted)
Memory:
  - Local JSON store (dev) or plug in Cosmos DB
```

---

## 🚀 Quickstart

### 1) Create a virtual env & install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 2) Configure environment
```bash
cp .env.example .env
# Fill Azure settings if you want live LLM and RAG
```

### 3) Run
```bash
streamlit run app/ui_streamlit.py
```

> No keys? No problem. ArcLight will run in **Demo Mode** with canned agent outputs so you can see the UX and flow.

---

## 🔧 Environment Variables

Copy `.env.example` and fill as needed.

**Required for live LLM**  
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_DEPLOYMENT`  (e.g., gpt-4o-mini)
- `AZURE_OPENAI_API_VERSION` (e.g., 2024-06-01)

**Optional for RAG**  
- `AZURE_SEARCH_ENDPOINT`  
- `AZURE_SEARCH_KEY`  
- `AZURE_SEARCH_INDEX`

---

## 📂 Repo Structure

```
ArcLight-Copilot/
├─ app/
│  └─ ui_streamlit.py
├─ arclight/
│  ├─ agents/
│  │  ├─ planner.py
│  │  ├─ researcher.py
│  │  └─ reviewer.py
│  ├─ chains/
│  │  └─ rag_chain.py
│  ├─ tools/
│  │  ├─ web_search.py
│  │  ├─ github_issues.py
│  │  └─ py_sandbox.py
│  ├─ models/
│  │  └─ llm.py
│  ├─ memory/
│  │  └─ conversation_store.py
│  └─ config.py
├─ tests/
│  ├─ test_tools.py
│  └─ eval_tasks/
│     └─ tasks.yaml
├─ .github/workflows/ci.yml
├─ .devcontainer/devcontainer.json
├─ Dockerfile
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
```

---

## 🖥️ Streamlit UI

- **Left sidebar**: Model/feature status, demo-mode toggle, export trace
- **Main**: Prompt box → live “Agent Log” → final answer with citations
- **RAG panel**: Shows retrieved docs (when Azure AI Search is configured)

---

## 🧪 Tests & Eval

- `tests/test_tools.py` – sanity checks for tools (no external calls in CI)
- `tests/eval_tasks/tasks.yaml` – sample eval tasks for regression checks

Run tests:
```bash
pytest -q
```

---

## 🔐 Security & Safety Notes

- Python sandbox is **restricted** (builtins off, tiny allowlist).
- Web search tool is a **stub** by default—swap with Tavily/SerpAPI for production.
- Do not store keys in code. Use `.env` or your secret manager.

---

## 🗺️ Roadmap

- [ ] Ingestion script to push PDFs/notes into Azure AI Search
- [ ] Richer reviewer with structured hallucination scoring
- [ ] Next.js UI option
- [ ] Trace export as shareable JSON (replay in UI)

---

## 🙌 Credits

Built using LangChain, Streamlit, and Azure services.
MIT Licensed.
