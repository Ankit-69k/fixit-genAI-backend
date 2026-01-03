import requests
from models.prompts import INTENT_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"

INTENT_SCORE = {
    "strong": (0.25, "Strong buying intent in notes"),
    "medium": (0.15, "Moderate buying intent in notes"),
    "weak": (0.05, "Weak or unclear intent")
}

def infer_intent(notes: str):
    payload = {
        "model": "mistral",
        "prompt": INTENT_PROMPT.format(notes=notes),
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 1
        }
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=10)
    resp.raise_for_status()

    output = resp.json()["response"].strip().lower()

    if output not in INTENT_SCORE:
        output = "weak"

    return INTENT_SCORE[output]
