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

CALL_EVAL_PROMPT = """
You are evaluating a real estate sales call.

Return ONLY valid JSON with this schema:
{{
  "quality_score": number between 0 and 1,
  "rapport_building": true/false,
  "need_discovery": true/false,
  "closing_attempt": true/false,
  "compliance_risk": true/false,
  "summary": "1-2 sentence summary",
  "next_actions": ["action1", "action2"]
}}

Rules:
- Do not add extra keys
- Do not explain
- Be conservative with compliance_risk

Transcript:
{transcript}
"""
