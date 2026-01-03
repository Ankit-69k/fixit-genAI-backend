from src.services.call_eval_service import evaluate_call

def handle_call_eval(payload):
    return evaluate_call(payload.transcript)
