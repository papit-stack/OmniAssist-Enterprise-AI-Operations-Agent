# OmniAssist — Enterprise AI Operations Agent

OmniAssist is a tool-equipped enterprise AI assistant built for **NovaTech Solutions**. It helps employees get accurate answers about company policies (leave, benefits, payroll, IT security, travel, and more) and perform workplace tasks such as managing their Google Calendar.

The agent is built on **LangChain / LangGraph**, uses a **hybrid RAG pipeline** (vector + BM25 + cross-encoder reranking) over company policy documents, and is exposed through a **FastAPI** backend with a **Streamlit** chat frontend. It ships with a **DeepEval**-based evaluation suite for retrieval, answer generation, and tool selection.

---

## Features

- **RAG-based policy lookup** — answers company-specific questions strictly from retrieved evidence, with query rewriting and hybrid retrieval (FAISS vector search + BM25, reranked with Cohere).
- **Calendar integration** — Google Calendar tools (create, update, list events) via the LangChain Google Community toolkit.
- **Tool-use agent** — LangGraph agent with automatic tool-calling plus a `calculator` utility tool.
- **Streaming chat API** — token streaming over a FastAPI `/chat` endpoint.
- **Conversation memory** — PostgreSQL-backed checkpointer (LangGraph `PostgresSaver`) for per-user threads.
- **Security controls**:
  - PII middleware (email redaction, credit-card masking, API-key blocking).
  - Prompt-injection guard that rejects requests trying to override instructions or reveal system prompts.
- **Evaluation suite** — DeepEval metrics for contextual precision/recall, faithfulness, answer relevancy, answer correctness, and tool correctness.
- **CLI + Web + UI** — run interactively from the terminal, via API, or through the Streamlit frontend.

---

## Architecture

```
                       ┌──────────────────────────────┐
  Streamlit UI ──────▶ │ FastAPI  /api/v1/chat        │
  (app/frontend.py)    │  (app/api/app.py, routes.py) │
                       └──────────────┬───────────────┘
                                      ▼
                    ┌─────────────────────────────────┐
                    │ LangGraph Agent (create_agent)  │
                    │  - PII + Security middleware    │
                    │  - PostgresSaver checkpointer   │
                    └──────────────┬─────────────────┘
                                   ▼
          ┌─────────────┬──────────┴───────────┐
          ▼             ▼                      ▼
   RAG Tool        Calendar Tools         Calculator
  (policies)       (Google Calendar)      (arithmetic)
          │
          ▼
  Query Rewriter → Hybrid Retriever → Reranker
  (LLM)          (FAISS + BM25)     (Cohere)
```

### Components

| Path | Description |
| --- | --- |
| `app/api/app.py` | FastAPI application with `/` and `/health` endpoints. |
| `app/api/routes.py` | `/api/v1/chat` — streaming chat endpoint. |
| `app/agents/agent.py` | The LangGraph agent: tool binding, security/PII middleware, streaming (`stream_agent`) and evaluation helpers (`test_agent`). |
| `app/main.py` | Standalone CLI loop using a hand-built LangGraph `StateGraph`. |
| `app/frontend.py` | Streamlit chat UI that streams from the FastAPI backend. |
| `app/rag/ingest.py` | Loads `.txt` policy docs from `app/data`, chunks, embeds, and saves a FAISS vector store. |
| `app/rag/retriever.py` | Hybrid retriever (FAISS + BM25, 70/30) with Cohere reranking. |
| `app/rag/query_rewriter.py` | LLM-based query rewriting using conversation context. |
| `app/rag/rag_tool.py` | `search_company_policies` LangChain tool wrapping the RAG pipeline. |
| `app/tools/` | Tool registry (`tools.py`) and Google Calendar toolkit wrapper (`calendar_tools.py`). |
| `app/evaluation/` | DeepEval suites for retrieval, answer generation, and tool selection. |
| `app/config.py` | Model names, embedding model, chunking, and paths. |
| `app/prompt.py` | System prompts (agent, query rewriter, RAG generator). |

---

## Tech Stack

- **Python 3.12**
- **LangChain / LangGraph** (agent framework, tool calling, checkpointer)
- **FastAPI + Uvicorn** (REST/streaming API)
- **Streamlit** (chat UI)
- **FAISS + BM25 + Cohere Rerank** (hybrid retrieval)
- **Sentence Transformers** (`all-MiniLM-L6-v2` embeddings)
- **Google GenAI (Gemini) / Groq** (LLMs, with fallbacks)
- **PostgreSQL / Supabase** (conversation checkpoints)
- **DeepEval** (evaluation)

---

## Prerequisites

- Python 3.12+
- PostgreSQL database (the app uses a Supabase Postgres connection) — used for the LangGraph checkpointer.
- Google Calendar OAuth credentials (`credentials.json` and `token.json`) for calendar tools.
- API keys for the LLM providers and Cohere reranking.

---

## Environment Variables

Create a `.env` file in the project root (`.env` is git-ignored). The following variables are used:

| Variable | Purpose |
| --- | --- |
| `GOOGLE_API_KEY` | Google GenAI (Gemini) model access. |
| `GROQ_API_KEY` | Groq fallback model access. |
| `DB_URL` | PostgreSQL connection string for the LangGraph checkpointer. |
| `CO_API_KEY` | Cohere reranking. |
| `HF_TOKEN` | Hugging Face token (embedding model downloads). |
| `OPENROUTER_API_KEY` | Optional; used by some evaluation judges. |
| `TAVILY_API_KEY` | Optional; reserved for web search. |

> **Note:** The current `.env`/`credentials.json`/`token.json` files contain live credentials. Keep them out of version control and rotate them if they are ever exposed.

---

## Installation & Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate      # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Copy/replace your .env values (GOOGLE_API_KEY, GROQ_API_KEY, DB_URL, CO_API_KEY, HF_TOKEN)
```

### Build / refresh the vector store

Run once (or whenever policy documents in `app/data/` change):

```bash
python -m app.rag.ingest
```

This loads all `.txt` files from `app/data/`, chunks them, and saves a FAISS index to `vector_db_faiss/`. To add a single new document to the existing store, see `add_new_document()` in `app/rag/ingest.py`.

---

## Running

### 1. FastAPI backend (required by the frontend)

```bash
uvicorn app.api.app:app --host 0.0.0.0 --port 8000 --reload
```

- Health check: `GET http://127.0.0.1:8000/health`
- Chat: `POST http://127.0.0.1:8000/api/v1/chat`

```bash
curl -N -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many days of earned leave do I get?", "user_id": "user-1"}'
```

### 2. Streamlit chat UI

```bash
streamlit run app/frontend.py
```

### 3. CLI agent

```bash
python -m app.main
```

---

## Running Evaluations

The evaluation suite uses [DeepEval](https://docs.confident-ai.com/) and LLM judges. Each script has two phases: build the test dataset (captures agent/retriever outputs into JSON) and evaluate.

```bash
# Retrieval quality (contextual precision / recall)
python -m app.evaluation.eval_retriever

# Answer generation (faithfulness, relevancy, correctness)
python -m app.evaluation.rag_evaluation

# Tool selection correctness
python -m app.evaluation.tool_selection
```

Note: `eval_retriever.py` uses a local Ollama judge (`llama3.2:3b` at `localhost:11434`); `rag_evaluation.py` and `tool_selection.py` use Gemini. Ensure the required judges and API keys are available.

---

## Docker

A `Dockerfile` is provided for the **FastAPI backend**.

```bash
# Build
docker build -t omniassist .

# Run (pass your secrets at runtime)
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=... \
  -e GROQ_API_KEY=... \
  -e DB_URL=... \
  -e CO_API_KEY=... \
  -e HF_TOKEN=... \
  -v "%cd%"/credentials.json:/app/credentials.json \
  -v "%cd%"/token.json:/app/token.json \
  omniassist
```

```bash
# Or with an env file
docker run -p 8000:8000 --env-file .env omniassist
```

Notes:

- The image installs from `requirements.txt` minus Windows-only packages (e.g. `pywin32`), so it runs on Linux.
- The prebuilt FAISS store in `vector_db_faiss/` is baked into the image; it can be replaced with a volume mount.
- `credentials.json` / `token.json` are the Google Calendar OAuth files — mount them as shown (the image excludes them via `.dockerignore`).
- The container needs outbound network access on first run to download the `all-MiniLM-L6-v2` embedding model into the HF cache.

---

## Project Structure

```
.
├── app/
│   ├── agents/          # LangGraph agent + streaming/eval helpers
│   ├── api/             # FastAPI app and /chat route
│   ├── data/            # Company policy documents (source for RAG)
│   ├── evaluation/      # DeepEval suites (retrieval, RAG, tools)
│   ├── rag/             # Ingest, retriever, query rewriter, RAG tool
│   ├── tools/           # Calculator + Google Calendar tools
│   ├── config.py        # Models, chunking, paths
│   ├── frontend.py      # Streamlit chat UI
│   ├── main.py          # CLI agent entry point
│   ├── models.py        # LLM factory with Gemini→Groq fallback
│   └── prompt.py        # System prompts
├── vector_db_faiss/     # Prebuilt FAISS index
├── requirements.txt
├── Dockerfile
└── .env                 # Local secrets (git-ignored)
```

---

## Security & Privacy Notes

- Responses are grounded in retrieved evidence; the agent is instructed never to fabricate company facts.
- Retrieved documents and user content are treated as data, not instructions (prompt-injection hardening).
- PII middleware redacts/masks/blocks emails, credit cards, and API keys in user input.
- Employee privacy is enforced (no cross-employee salary/calendar/benefit disclosure).

---

## License

No license is specified in this repository.