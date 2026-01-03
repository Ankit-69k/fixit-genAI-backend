import pytest
from src.schemas.lead import Lead
from src.services.priority_engine import compute_priority

def test_high_quality_lead_scores_hot():
    lead = Lead(
        lead_id="L1",
        source="website",
        budget=9_000_000,
        city="Bangalore",
        property_type="3BHK",
        last_activity_minutes_ago=10,
        past_interactions=4,
        notes="Ready to buy and close fast",
        status="follow_up"
    )

    result = compute_priority(lead)

    assert result["priority_bucket"] == "hot"
    assert 0.7 <= result["priority_score"] <= 1.0
    assert "High budget" in result["reasons"]
    assert any("intent" in r.lower() for r in result["reasons"])


def test_low_quality_lead_scores_cold():
    lead = Lead(
        lead_id="L2",
        source="portal",
        budget=None,
        city="Delhi",
        property_type="1BHK",
        last_activity_minutes_ago=2000,
        past_interactions=0,
        notes="Just browsing, will think later",
        status="new"
    )

    result = compute_priority(lead)

    assert result["priority_bucket"] == "cold"
    assert result["priority_score"] < 0.4
