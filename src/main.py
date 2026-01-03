from fastapi import FastAPI
from src.api.v1.lead_priority import router as lead_router

app = FastAPI(title="Lead Intelligence API")

app.include_router(lead_router)
