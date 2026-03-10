from fastapi import FastAPI
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from profile import build_user_profile
from memory import ConversationMemory
from intent import detect_intent, should_retrieve
from retriever import Retriever

from openai import OpenAI
import os

# ---------- OPTIONAL: OpenAI ----------
# Uncomment if using OpenAI
# from dotenv import load_dotenv
# from openai import OpenAI
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# -------------------------------------


app = FastAPI()

memory = ConversationMemory()
retriever = Retriever()


class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_profile: dict


@app.get("/")
def home():
    return {"message": "Astro Conversational Agent Running"}


# ---------- LLM PROVIDERS ----------

def generate_openai(prompt):
    """
    Use OpenAI API
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_ollama(prompt):
    """
    Use local Ollama model
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral-nemo",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# ---------- SELECT MODEL HERE ----------
# Choose ONE

LLM_PROVIDER = "ollama"
# LLM_PROVIDER = "openai"
# --------------------------------------


def generate_response(prompt):

    if LLM_PROVIDER == "openai":
        return generate_openai(prompt)

    if LLM_PROVIDER == "ollama":
        return generate_ollama(prompt)

    raise ValueError("Invalid LLM provider")


@app.post("/chat")
def chat(request: ChatRequest):

    # Build user profile
    profile = build_user_profile(request.user_profile)

    # Retrieve conversation history
    history_list = memory.get_history(request.session_id)

    history = ""
    for turn in history_list:
        history += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    # Detect intent
    intent = detect_intent(request.message)
    print("INTENT:", intent) 
    
    context_docs = []
    context_sources = []

    # ---------- SUMMARY HANDLING ----------
    if intent == "summary":
         
        history =memory.get_history(request.session_id)

        summary = "Here's a summary of our conversation so far:\n\n"

        i = 1
        for turn in history:

            # Skip previous summary requests
            if "summarize" in turn["user"].lower():
                continue

            summary += f"{i}. User asked: {turn['user']}\n"
            summary += f"   I responded: {turn['assistant'][:120]}...\n\n"

            i += 1
        return {
            "response": summary,
            "zodiac": profile["zodiac"],
            "context_used": [],
            "retrieval_used": False
        }
    # -------------------------------------

    context_docs = []
    context_sources = []

    if should_retrieve(intent):
        context_docs, context_sources = retriever.retrieve(request.message)

    context_text = "\n".join(context_docs)

    # Build prompt
    prompt = f"""
You are an astrology assistant that answers questions using retrieved astrology knowledge.

Rules:
1. Use ONLY the astrology knowledge provided below when answering.
2. If the answer is not present in the knowledge base, say you do not have enough information.
3. Use the conversation history to understand follow-up questions.
4. Keep responses concise and helpful.

User zodiac: {profile['zodiac']}

Conversation history:
{history}

Astrology knowledge:
{context_text}

User question:
{request.message}

Give a helpful explanation grounded in astrology knowledge.
"""

    # Hindi support
    if profile["preferred_language"] == "hi":
        prompt += "\nRespond in Hindi."

    # Generate LLM response
    answer = generate_response(prompt)

    # Save conversation memory
    memory.add_turn(request.session_id, request.message, answer)

    return {
        "response": answer,
        "zodiac": profile["zodiac"],
        "context_used": context_sources,
        "retrieval_used": should_retrieve(intent)
    }