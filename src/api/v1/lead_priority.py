from fastapi import APIRouter
from src.schemas.lead import LeadPriorityRequest
from src.handlers.lead_priority_handler import rank_leads

router = APIRouter(prefix="/api/v1", tags=["Lead Priority"])

@router.post("/lead-priority")
def lead_priority(payload: LeadPriorityRequest):
    results = rank_leads(payload.leads, payload.max_results)
    return {"results": results}
