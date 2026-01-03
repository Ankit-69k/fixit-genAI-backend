from pydantic import BaseModel, Field
from typing import List, Optional

class Lead(BaseModel):
    lead_id: str
    source: str
    budget: Optional[float]
    city: str
    property_type: str
    last_activity_minutes_ago: Optional[int]
    past_interactions: int
    notes: str
    status: str

class LeadPriorityRequest(BaseModel):
    leads: List[Lead]
    max_results: int = Field(default=10, le=50)
