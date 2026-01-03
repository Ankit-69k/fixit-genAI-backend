def rule_score(lead):
    score = 0.0
    reasons = []

    if lead.budget and lead.budget > 7_000_000:
        score += 0.25
        reasons.append("High budget")

    if lead.last_activity_minutes_ago is not None:
        if lead.last_activity_minutes_ago < 60:
            score += 0.25
            reasons.append("Very recent activity")
        elif lead.last_activity_minutes_ago < 300:
            score += 0.15
            reasons.append("Recent activity")

    if lead.past_interactions >= 3:
        score += 0.15
        reasons.append("Multiple interactions")

    if lead.status == "follow_up":
        score += 0.1
        reasons.append("Pending follow-up")

    return score, reasons
