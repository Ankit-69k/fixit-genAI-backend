from fastapi import FastAPI
from src.api.v1.lead_priority import router as lead_router
from src.api.v1.call_eval import router as call_router

app = FastAPI(title="Lead Intelligence API")

app.include_router(lead_router)
app.include_router(call_router)