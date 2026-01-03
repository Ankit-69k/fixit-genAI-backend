from src.utils.rules import rule_score
from models.intent_model import infer_intent

def compute_priority(lead):
    score = 0.0
    reasons = []

    r_score, r_reasons = rule_score(lead)
    score += r_score
    reasons.extend(r_reasons)

    i_score, i_reason = infer_intent(lead.notes)
    score += i_score
    reasons.append(i_reason)

    score = min(score, 1.0)

    bucket = (
        "hot" if score >= 0.7 else
        "warm" if score >= 0.4 else
        "cold"
    )

    return {
        "lead_id": lead.lead_id,
        "priority_score": round(score, 2),
        "priority_bucket": bucket,
        "reasons": reasons
    }
