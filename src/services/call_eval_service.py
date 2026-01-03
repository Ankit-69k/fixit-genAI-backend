import json
from models.llm_service import call_llm
from src.utils.logger import logger

def evaluate_call(transcript: str):
    """
    Analyzes a call transcript using an LLM and returns structured evaluation metrics.
    Logs latency, input size, and errors as required.
    """
    input_size = len(transcript)

    try:
        raw_output, latency = call_llm(transcript)
        
        # Robust parsing of LLM response
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError as je:
            logger.error(f"llm_parse_failed | error={je} | raw_output={raw_output}")
            raise RuntimeError("Failed to parse LLM response as JSON")

        logger.info(
            f"call_eval success | latency_ms={latency} | input_chars={input_size}"
        )

        # Map labels safely
        labels = {
            "rapport_building": bool(parsed.get("rapport_building", False)),
            "need_discovery": bool(parsed.get("need_discovery", False)),
            "closing_attempt": bool(parsed.get("closing_attempt", False)),
            "compliance_risk": bool(parsed.get("compliance_risk", False)),
        }

        return {
            "quality_score": round(float(parsed.get("quality_score", 0.0)), 2),
            "labels": labels,
            "summary": parsed.get("summary", "No summary provided"),
            "next_actions": parsed.get("next_actions", []),
            "model_metadata": {
                "model_name": "mistral",
                "latency_ms": latency
            }
        }

    except Exception as e:
        logger.error(
            f"call_eval failed | error={e} | input_chars={input_size}"
        )
        raise
