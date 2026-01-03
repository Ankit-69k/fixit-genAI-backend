import requests
import time
from models.prompts import INTENT_PROMPT, CALL_EVAL_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

INTENT_SCORE = {
    "strong": (0.25, "Strong buying intent in notes"),
    "medium": (0.15, "Moderate buying intent in notes"),
    "weak": (0.05, "Weak or unclear intent")
}

def infer_intent(notes: str):
    payload = {
        "model": MODEL_NAME,
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

def call_llm(transcript: str, retries: int = 2):
    payload = {
        "model": MODEL_NAME,
        "prompt": CALL_EVAL_PROMPT.format(transcript=transcript),
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    last_error = None

    for attempt in range(retries + 1):
        start = time.time()
        try:
            # Increased timeout for longer transcripts
            resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
            latency = int((time.time() - start) * 1000)
            resp.raise_for_status()

            data = resp.json()["response"]
            
            # Simple heuristic to extract JSON if model wraps it in markdown
            if "```json" in data:
                data = data.split("```json")[1].split("```")[0].strip()
            elif "```" in data:
                data = data.split("```")[1].split("```")[0].strip()
            
            return data.strip(), latency

        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1) # Short backoff

    raise RuntimeError(f"LLM failed after {retries} retries: {last_error}")