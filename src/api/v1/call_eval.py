from fastapi import APIRouter
from src.schemas.call import CallEvalRequest
from src.handlers.call_eval_handler import handle_call_eval

router = APIRouter(prefix="/api/v1", tags=["Call Evaluation"])

@router.post("/call-eval")
def call_eval(payload: CallEvalRequest):
    return handle_call_eval(payload)
