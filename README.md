# Astro Conversational Insight Agent

This project implements a **multi-turn astrology chatbot** using **Retrieval Augmented Generation (RAG)** with conversation memory.

The system demonstrates conversation ownership, intent-aware retrieval, and personalized responses based on user birth details.

---

# Features

* FastAPI-based chat API
* Session-based conversation memory
* Intent-aware retrieval (RAG)
* Vector search using FAISS
* Zodiac-based personalization
* Multi-turn conversational reasoning
* Optional LLM providers (OpenAI API or Local LLM via Ollama)

---
# Api interface
<img width="1229" height="1267" alt="image" src="https://github.com/user-attachments/assets/c87d4201-4afb-4d69-82a0-53599f56cdd9" />

---

# Project Structure

```
astro_agent
│
├── app.py
├── intent.py
├── memory.py
├── profile.py
├── retriever.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── career_guidance.txt
│   ├── love_guidance.txt
│   ├── spiritual_guidance.txt
│   ├── planetary_impacts.json
│   ├── zodiac_traits.json
│   └── nakshatra_mapping.json
│
└── evaluation/
    └── rag_evaluation.md
```

---

# Installation

Install the required dependencies:

```
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the root directory of the project.

Example:

```
OPENAI_API_KEY=your_openai_api_key_here
```

This is required **only if using OpenAI API as the LLM provider**.

---

# LLM Provider Options

The system allows switching between **OpenAI API** and a **local LLM using Ollama**.

### Option 1 — OpenAI API

In `app.py`, set:

```
LLM_PROVIDER = "openai"
```

Ensure your `.env` file contains a valid OpenAI API key.

---

### Option 2 — Local LLM (Ollama)

If you prefer to run a local model using Ollama, set:

```
LLM_PROVIDER = "ollama"
```

Make sure Ollama is installed and running locally with a model available.

Example models:

* mistral
* mistral-nemo
* llama3

You can change the model name inside `generate_ollama()` in `app.py`.

---

# Running the API

Start the FastAPI server:

```
uvicorn app:app --reload
```

Open the API documentation:

```
http://127.0.0.1:8000/docs
```

This provides an interactive interface to test the chatbot.

---

# Example Request

Example request body:

```
{
  "session_id": "abc-123",
  "message": "How will my month be in career?",
  "user_profile": {
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "preferred_language": "en"
  }
}
```

---

# System Components

### User Profile Builder

Extracts user zodiac sign from birth date and builds a profile used for personalization.

---

### Conversation Memory

Stores multi-turn conversation history using `session_id`.

This allows the chatbot to maintain context across multiple questions.

---

### Intent Detection

Detects the user's query intent to determine whether retrieval is required.

Examples:

* career guidance
* relationship questions
* planetary influence
* summary requests

---

### Retrieval Layer

Uses sentence-transformer embeddings and FAISS vector search to retrieve relevant astrology knowledge.

Retrieval is **intent-aware**, meaning it is triggered only when additional knowledge is needed.

---

### LLM Response Generation

The system supports two LLM providers:

* OpenAI API
* Local LLM via Ollama

The provider can be selected by changing the `LLM_PROVIDER` variable in `app.py`.

---

# Evaluation

The `evaluation` folder contains a brief analysis of the RAG system including:

* Cases where retrieval improves answer quality
* Cases where retrieval may introduce irrelevant context
* Trade-offs between always-on retrieval vs intent-aware retrieval

---

# Notes
* Dependencies can be installed using the provided `requirements.txt`.

---

# Summary

This project demonstrates a conversational AI system capable of:

* Maintaining session-based memory
* Performing intent-aware knowledge retrieval
* Generating personalized astrology insights
* Supporting both cloud-based and local LLM deployments
