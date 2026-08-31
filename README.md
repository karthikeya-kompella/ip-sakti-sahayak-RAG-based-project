# IP-SAKTI Sahayak

A multilingual, RAG-based (source-cited) AI assistant for Intellectual Property and regulatory guidance in Ayurveda, across national and international regulatory regimes.

## Overview

Ayurveda sits at a complex intersection of traditional knowledge, drug regulation, and intellectual property law. A single formulation can be treated entirely differently depending on jurisdiction — for example, excluded from patentability under Section 3(p) of India's Patents Act, while requiring FDA botanical drug or dietary supplement approval in the United States.

IP-SAKTI Sahayak answers these questions directly from real regulatory source documents — not from a language model's memory — with every answer traceable back to its exact source text. Users can query a single jurisdiction or request a side-by-side comparison across regimes.

## Why RAG, not a plain LLM or fine-tuning

- **Grounding:** answers are generated only from retrieved source documents, reducing hallucination risk in a domain where incorrect legal/regulatory claims carry real consequences
- **Traceability:** every claim is citable back to a specific document and passage — essential for legal/regulatory trust
- **Updatability:** new regulations can be ingested at any time without retraining a model
- **Multi-jurisdiction by design:** retrieval is filtered by regime metadata, enabling accurate, scoped answers per country

## Features

- Multilingual retrieval using a single shared embedding space (Hindi + English), avoiding lossy translation steps
- Regime-filtered semantic search (currently: India–AYUSH, United States–FDA)
- Compare mode: retrieves and answers per jurisdiction, then synthesizes agreements/differences across regimes
- Source-cited responses — every answer includes the original chunk text, document title, language, and source URL
- JWT-based authentication
- Document ingestion pipeline with regime/language/doc-type metadata tagging

## Tech Stack

**Backend**
- Python, FastAPI
- PostgreSQL (SQLAlchemy ORM)
- ChromaDB (vector database, cosine similarity search)
- Embeddings: [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) (multilingual)
- LLM generation via [OpenRouter](https://openrouter.ai)
- JWT authentication (python-jose, passlib)
- PDF text extraction (pypdf)

**Frontend**
- React + Vite

## Architecture

```
Document Ingestion:
  PDF → text extraction → chunking (with overlap) → 
  regime/language/doc-type metadata tagging → 
  embedding (bge-m3) → stored in ChromaDB

Query:
  User question → embedded → regime-filtered semantic 
  search (cosine similarity, top-k) → relevant chunks retrieved

Generation:
  Retrieved chunks + question → LLM (strictly grounded prompt) → 
  answer + citations returned

Compare Mode:
  Retrieval + generation run independently per selected regime → 
  per-regime answers synthesized into a cross-jurisdiction comparison
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Create a new user account |
| POST | `/api/v1/auth/login` | Authenticate and receive a JWT (OAuth2 form data) |
| GET | `/api/v1/regimes` | List available regulatory jurisdictions |
| POST | `/api/v1/documents/upload` | Ingest a new document (PDF) with regime/language/doc-type metadata |
| GET | `/api/v1/documents` | List ingested documents, optionally filtered by regime |
| POST | `/api/v1/query` | Ask a question scoped to a single jurisdiction |
| POST | `/api/v1/query/compare` | Ask a question and compare answers across multiple jurisdictions |

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Node.js (for frontend)

### Backend

```bash
git clone <repo-url>
cd ip-sakti-backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file:
```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/ipsakti
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<your-random-secret-key>
CHROMA_PERSIST_DIR=./chroma_data
EMBEDDING_MODEL_NAME=BAAI/bge-m3
OPENROUTER_API_KEY=<your-openrouter-key>
GENERATION_MODEL_NAME=<your-chosen-model-slug>
```

Run the server:
```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd ip-sakti-sahayak-frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## Current Scope

- Regimes covered: India (AYUSH), United States (FDA)
- Retrieval method: pure semantic (cosine similarity) search
- Ingestion: synchronous, PDF-based

## Roadmap

- Hybrid retrieval (BM25 + semantic search) via Reciprocal Rank Fusion, for improved exact-citation matching
- Reranking of retrieved chunks before generation
- OCR pipeline for scanned/image-based government documents
- Additional regulatory regimes (EU, China, etc.)
- Dedicated non-English document corpus for extended multilingual validation
- Automatic jurisdiction detection from query text
- Conversation history and multi-turn context

## Disclaimer

IP-SAKTI Sahayak provides informational guidance grounded in ingested regulatory documents. It is not a substitute for professional legal advice.

## Author

Kompella Sri Sai Satya Karthikeya
