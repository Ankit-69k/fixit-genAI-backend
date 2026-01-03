from pydantic import BaseModel
from typing import List, Dict

class CallEvalRequest(BaseModel):
    call_id: str
    lead_id: str
    transcript: str
    duration_seconds: int

class CallEvalResponse(BaseModel):
    quality_score: float
    labels: Dict[str, bool]
    summary: str
    next_actions: List[str]
    model_metadata: Dict[str, str | int]
