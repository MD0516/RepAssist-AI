# RepAssist AI — HCP Log Interaction Screen

An AI-first CRM module for pharmaceutical field representatives to log, edit, and review interactions with Healthcare Professionals (HCPs) — driven entirely by a conversational AI assistant rather than manual form entry.

Built for the AI-First CRM HCP Module technical assignment.

---

## Overview

Field reps typically log HCP visits through tedious structured forms. This project replaces manual data entry with a **LangGraph-powered AI agent**: the rep simply describes what happened in natural language, and the agent extracts, structures, edits, and retrieves interaction records on their behalf.

The screen is a two-panel layout:
- **Left panel** — Interaction Details. Read-only to the user; populated and updated exclusively by the AI agent.
- **Right panel** — AI Assistant chat. The only interface through which the rep interacts with the system.

---

## Architecture

```
User (chat message)
      │
      ▼
Frontend (React + Redux) ── POST /chat ──▶ FastAPI backend
                                                  │
                                                  ▼
                                          LangGraph Agent
                                    ┌─────────────┼─────────────┐
                                    │             │             │
                                 router  →  toolExecutor  →  responseGenerator
                                                  │
                                    ┌─────────────┼──────────────────────┐
                                    ▼             ▼                      ▼
                            logInteraction  editInteraction   suggestFollowUp
                                    listInteractions        callPrep
                                                  │
                                                  ▼
                                          PostgreSQL (via SQLAlchemy)
```

The router node uses an LLM call to select the appropriate tool for each user message. It enforces a simple policy: without an active interaction, only `logInteraction` and `listInteractions` are valid choices; once an interaction exists, all five tools become available.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Redux Toolkit, Bootstrap, Google Inter |
| Backend | Python, FastAPI |
| AI Agent Framework | LangGraph |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Database | PostgreSQL (via SQLAlchemy) |

---

## The 5 LangGraph Tools

| Tool | Purpose |
|---|---|
| **logInteraction** | Extracts a new interaction record (HCP name, product discussed, sentiment, materials shared, discussion points) from a natural-language description, using LLM structured output. |
| **editInteraction** | Updates only the fields explicitly mentioned in a natural-language correction, leaving all other data on the record untouched. |
| **suggestFollowUp** | Analyzes the current interaction's sentiment and content, and generates a follow-up recommendation written back onto the record. |
| **callPrep** | Retrieves an HCP's full interaction history and generates a briefing — prior topics, materials already shared, sentiment trend, talking points, and next-best-action — ahead of the rep's next visit. |
| **listInteractions** | Converts a natural-language query into structured search filters and returns matching interaction records; the frontend renders these as a clickable table. |

All tool logic runs through the LLM using schema-constrained structured output (Pydantic models) — no keyword matching or regex-based extraction is used for understanding user input.

---

## Project Structure

```
AIVOA-CRM/
├── backend/
│   ├── app/
│   │   ├── agents/        # LangGraph graph, nodes, router, state
│   │   ├── api/           # FastAPI routes (chat, interactions)
│   │   ├── core/          # config/settings
│   │   ├── db/            # database session & base
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── services/      # Groq LLM service, interaction service
│   │   └── tools/         # the 5 LangGraph tools
│   ├── main.py
│   ├── create_tables.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/    # interaction panel, chat panel, table, etc.
│   │   ├── pages/         # HCPInteractionPage
│   │   ├── redux/         # interaction & chat slices, store
│   │   ├── layouts/       # DashboardLayout
│   │   └── services/      # api.js
│   ├── package.json
│   └── .env.example
└── README.md
```

---

## Setup & Running Locally

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL running locally or a hosted instance (e.g. Neon, Supabase)
- A free Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/MD0516/RepAssist-AI.git
cd RepAssist-AI
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/aivoa_crm
```

**First run only:** create the database tables by running the setup script:
```bash
python create_tables.py
```
This only needs to be run once, before starting the server for the first time.

Run the backend:
```bash
uvicorn main:app --reload
```
Backend runs at `http://localhost:8000`.

### 3. Frontend setup
```bash
cd frontend
npm install
```

Copy `.env.example` to `.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

Run the frontend:
```bash
npm run dev
```
Frontend runs at `http://localhost:5173` (default Vite port).

### 4. Open the app
Visit `http://localhost:5173` in your browser. Start by describing an interaction in the AI Assistant chat panel — e.g. *"Met Dr. Sharma today, discussed the new cardio drug, she was positive, shared the brochure."*

---

## Known Limitations

- The interaction schema was intentionally kept to core fields (HCP name, date, type, product, sentiment, materials, discussion points, follow-up) rather than every field shown in the original task mockup, to keep the focus on demonstrating genuine LLM-driven tool behavior rather than form breadth.
- Error handling on API failure in the frontend currently surfaces an error message but does not automatically retry.
- No authentication/multi-user support — this is a single-session prototype scoped to the assignment.

---

## What This Demonstrates

This project treats the LangGraph agent as the primary interface for structured CRM data entry, not a bolt-on chatbot. Every field on the Interaction Details panel is populated or modified exclusively through natural language, with the agent responsible for extraction (Log), precise partial updates (Edit), proactive reasoning (Suggest Follow-Up, Call Prep), and retrieval (List Interactions) — all backed by LLM structured output rather than hard-coded parsing logic.