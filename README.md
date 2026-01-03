# Fixit GenAI Backend Assignment

This repository contains a **FastAPI-based backend** demonstrating **scalable, explainable GenAI-powered APIs** using **open-source LLMs**.

The system exposes two primary capabilities:

- **Lead Prioritization** using deterministic business rules combined with LLM-based interpretation of unstructured notes
- **Sales Call Evaluation** using structured LLM analysis with retries, latency tracking, and graceful fallbacks

The design explicitly prioritizes **determinism, explainability, and reliability** over opaque AI-only decision making.

---

## 📦 Tech Stack

- **FastAPI** – API framework
- **Pydantic** – request/response validation
- **Ollama** – local OSS LLM runtime
- **Mistral** – open-source LLM
- **Docker** – containerization
- **Python 3.12.12**

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.10+
- Ollama installed
- Mistral model pulled

### Install & Run Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
ollama serve
```

Verify Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

---

### Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Run the Application

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```text
fixit-backend-assignment/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── lead_priority.py      # Lead ranking endpoints
│   │       └── call_eval.py          # Call quality evaluation endpoints
│   │
│   ├── handlers/
│   │   ├── lead_priority_handler.py  # Request orchestration
│   │   └── call_eval_handler.py
│   │
│   ├── services/
│   │   ├── priority_engine.py        # Core lead scoring logic
│   │   └── call_eval_service.py      # Call evaluation workflow
│   │
│   ├── schemas/
│   │   ├── lead.py                   # Lead request/response models
│   │   └── call.py                   # Call evaluation schemas
│   │
│   ├── utils/
│   │   ├── rules.py                  # Deterministic scoring rules
│   │   └── logger.py                 # Centralized logging
│   │
│   └── main.py                       # FastAPI application entry point
│
├── models/
│   ├── llm_client.py                 # Ollama (Mistral) LLM HTTP client
│   └── prompts.py                    # Strict, deterministic LLM prompts
│
├── data/
│   ├── leads.csv                     # Sample lead dataset
│   └── calls.json                    # Sample call transcripts
│
├── tests/
│   └── test_api.py                   # Unit tests
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🏗️ Architecture Overview

```text
┌───────────────┐
│   Client /    │
│   Consumer    │
└───────┬───────┘
        │ HTTP
        ▼
┌──────────────────────┐
│      FastAPI API     │
│  (src/api/v1/*)      │
└────────┬─────────────┘
         ▼
┌─────────────────────────┐
│       Handlers          │
│ (Request Orchestration) │
└────────┬────────────────┘
         ▼
┌──────────────────────┐
│       Services       │
│ (Business Logic)     │
│  - Priority Engine   │
│  - Call Evaluation   │
└────────┬─────────────┘
         │
   ┌─────▼───────────┐
   │ Deterministic   │
   │ Rules Engine    │
   │ (utils/rules)   │
   └─────────────────┘
         │
   ┌─────▼───────────┐
   │  LLM Client     │
   │ (Ollama/Mistral)│
   │  models/*       │
   └─────────────────┘
         │
         ▼
┌──────────────────────┐
│   Ollama HTTP API    │
│  (localhost:11434)   │
└──────────────────────┘
```

---

## 🧠 Architectural Principles

- **Separation of Concerns**  
  API routing, orchestration, business logic, and AI integration are isolated into distinct layers.

- **LLM as Interpreter, Not Decision Maker**  
  Deterministic rules control final outcomes; the LLM only interprets unstructured text.

- **Determinism & Testability**  
  Fixed prompts, `temperature = 0`, bounded scoring, retries, and fallbacks ensure predictable behavior.

- **OSS-First Design**  
  Uses open-source models (Mistral via Ollama) with no vendor lock-in.

- **Production-Oriented Reliability**  
  Retry logic, latency logging, environment-based configuration, and graceful degradation are built in.

---

## 🔌 API Endpoints

### 1️⃣ Lead Priority API

**Endpoint**

```
POST /api/v1/lead-priority
```

**Purpose**  
Ranks leads based on structured attributes and LLM-derived intent from free-text notes.

#### Request Body

```json
{
  "max_results": 3,
  "leads": [
    {
      "lead_id": "L1001",
      "source": "website",
      "budget": 9000000,
      "city": "Bangalore",
      "property_type": "3BHK",
      "last_activity_minutes_ago": 15,
      "past_interactions": 4,
      "notes": "Client is ready to buy and wants to close fast",
      "status": "follow_up"
    }
  ]
}
```

#### Response

```json
{
  "results": [
    {
      "lead_id": "L1001",
      "priority_score": 0.9,
      "priority_bucket": "hot",
      "reasons": [
        "High budget",
        "Very recent activity",
        "Multiple interactions",
        "Pending follow-up",
        "Strong buying intent in notes"
      ]
    }
  ]
}
```

---

### 2️⃣ Call Evaluation API

**Endpoint**

```
POST /api/v1/call-eval
```

**Purpose**  
Evaluates sales call quality using an OSS LLM and returns structured QA signals.

#### Request Body

```json
{
  "call_id": "C1001",
  "lead_id": "L1001",
  "duration_seconds": 620,
  "transcript": "Agent: Hello. Buyer: I am interested in a 3BHK. Agent: What is your budget?"
}
```

#### Response

```json
{
  "quality_score": 0.78,
  "labels": {
    "rapport_building": true,
    "need_discovery": true,
    "closing_attempt": false,
    "compliance_risk": false
  },
  "summary": "Agent established rapport and discovered needs but did not attempt closing.",
  "next_actions": ["Schedule follow-up call", "Discuss pricing options"],
  "model_metadata": {
    "model_name": "mistral",
    "latency_ms": 842
  }
}
```

---

## 🐳 How to Run via Docker

### Build the Image

```bash
docker build -t fixit-genai-assignment .
```

---

### Run the Container

Ollama runs on the **host**, so its URL is passed via environment variables.

```bash
docker run -p 8000:8000 \
  -e OLLAMA_URL=http://host.docker.internal:11434/api/generate \
  -e OLLAMA_MODEL=mistral \
  fixit-genai-assignment
```

#### Linux / Fedora Alternative

```bash
docker run --network=host fixit-genai-assignment
```

---

## 🤖 Model Used & Rationale

### Model

- **Mistral (via Ollama)**

### Why Mistral

- Fully **open-source**
- Runs **locally** (no API keys, no vendor lock-in)
- Strong performance on:
  - summarization
  - intent classification
  - structured JSON generation
- Deterministic enough with `temperature = 0`

### How the Model Is Used

- LLMs are used **only for interpretation of unstructured text**
- Final decisions and scores remain **rule-based**
- Prevents hallucinations from directly influencing business logic

---

## ⚖️ Trade-offs & Design Decisions

### What Was Prioritized

- Determinism and explainability
- Clear separation of concerns
- OSS-only LLM usage
- Production-style retries, timeouts, and logging

### Trade-offs Made

- LLM calls are synchronous (simpler, but slower under load)
- Ollama runs outside Docker (lighter container, requires host setup)
- Prompt-based JSON parsing (robust for demo; schema validation could be added)

### Future Improvements

- Async/background inference
- Queue-based call evaluation
- Strict JSON schema validation for LLM outputs
- Metrics & tracing (Prometheus / OpenTelemetry)
- Horizontal scaling with worker pools

---

## 🧠 Architectural Summary

This backend demonstrates how to integrate open-source LLMs into a production-style system by treating them as **interpreters rather than decision-makers**, ensuring the system remains **explainable, testable, and resilient**.

---
