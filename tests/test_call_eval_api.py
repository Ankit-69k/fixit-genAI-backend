from fastapi.testclient import TestClient
from unittest.mock import patch
import json

from src.main import app

client = TestClient(app)

MOCK_LLM_RESPONSE = json.dumps({
    "quality_score": 0.8,
    "rapport_building": True,
    "need_discovery": True,
    "closing_attempt": False,
    "compliance_risk": False,
    "summary": "Agent built rapport and identified needs.",
    "next_actions": ["Schedule follow-up"]
})


@patch("src.services.call_eval_service.call_llm")
def test_call_eval_output_structure(mock_call_llm):
    mock_call_llm.return_value = (MOCK_LLM_RESPONSE, 500)

    payload = {
        "call_id": "C1",
        "lead_id": "L1",
        "duration_seconds": 600,
        "transcript": "Agent: Hello. Buyer: I am interested in a 2BHK."
    }

    response = client.post("/api/v1/call-eval", json=payload)

    assert response.status_code == 200

    data = response.json()

    # Top-level keys
    assert "quality_score" in data
    assert "labels" in data
    assert "summary" in data
    assert "next_actions" in data
    assert "model_metadata" in data

    # Labels structure
    labels = data["labels"]
    assert isinstance(labels["rapport_building"], bool)
    assert isinstance(labels["need_discovery"], bool)
    assert isinstance(labels["closing_attempt"], bool)
    assert isinstance(labels["compliance_risk"], bool)

    # Metadata
    assert data["model_metadata"]["model_name"] == "mistral"
    assert isinstance(data["model_metadata"]["latency_ms"], int)
