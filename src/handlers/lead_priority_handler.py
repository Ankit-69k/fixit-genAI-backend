from src.services.priority_engine import compute_priority

def rank_leads(leads, max_results):
    scored = []
    for lead in leads:
        scored.append(compute_priority(lead))

    scored.sort(key=lambda x: x["priority_score"], reverse=True)

    return scored[:max_results]
