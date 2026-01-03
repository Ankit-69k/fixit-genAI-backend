INTENT_PROMPT = """
You are a classifier.

Classify buyer intent from the notes into one label:
- strong
- medium
- weak

Rules:
- Respond with ONLY the label.
- No punctuation.
- No explanation.

Notes:
{notes}
"""
