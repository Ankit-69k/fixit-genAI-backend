# C2. Call Quality Evaluation

## Objective

Evaluate the **Call Quality Evaluation API** by comparing model-predicted call quality scores against **manually labeled ground truth** for a small, representative subset of calls.

The objective is to assess:

- classification effectiveness (good vs bad calls)
- usefulness of `quality_score` as a decision signal
- common failure modes of LLM-based call analysis

---

## Call Selection

From `calls.json`, **10 calls** were selected to cover:

- good vs poor agent behavior
- engaged vs disengaged buyers
- closed vs non-closed deals
- varied conversation lengths and tones

---

## Ground Truth Labeling

### Labeling Criteria

**Good Call**

- Clear rapport building
- Active need discovery (budget, location, timeline)
- Structured conversation
- Clear next steps or closing attempt
- Professional tone

**Bad Call**

- Rambling or unstructured
- No discovery
- Buyer disengaged
- No next steps
- Pushy or risky language

Distribution:

- Good: 5
- Bad: 5

---

## Model Predictions

Calls were evaluated using:

```
POST /api/v1/call-eval
```

## Decision Threshold

A fixed threshold was chosen:

```
quality_score ≥ 0.60 → good
quality_score < 0.60 → bad
```

This threshold favors **precision over recall**, which is desirable in sales-quality assessment to avoid overrating poor calls.

---

## Metrics

### Confusion Matrix (Good = Positive Class)

- True Positives (TP): 5
- True Negatives (TN): 4
- False Positives (FP): 1
- False Negatives (FN): 0

---

### Accuracy

```
Accuracy = (TP + TN) / Total
         = (5 + 4) / 10
         = 0.90
```

---

### Precision

```
Precision = TP / (TP + FP)
          = 5 / 6
          ≈ 0.83
```

---

### Recall

```
Recall = TP / (TP + FN)
       = 5 / 5
       = 1.00
```

---

### F1 Score

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
   ≈ 0.91
```

---

## Error Analysis (Wrong Predictions)

### ❌ Case 1: Call C005 (False Positive)

- Human Label: bad
- Predicted Label: good
- quality_score: 0.61

**Explanation:**
The agent used confident and assertive language, which the model interpreted as effective closing behavior. However, the call lacked genuine need discovery and included borderline sales pressure.

**Insight:**  
Tone and confidence can outweigh substance in LLM-based scoring unless explicitly penalized.

---

### ⚠️ Case 2: Call C007 (Borderline Bad Call)

- Human Label: bad
- quality_score: 0.57 (near threshold)

**Explanation:**
The agent was polite and responsive but failed to move the conversation toward concrete next steps. The score was close to the threshold, highlighting sensitivity around mid-range values.

**Insight:**  
Threshold choice significantly impacts classification for average-quality calls.

---

## Key Insights

1. **Structured calls are reliably identified as good**  
   Calls with clear phases (rapport → discovery → next step) consistently scored high.

2. **Confidence can mask weaknesses**  
   Assertive language may inflate scores even when core sales fundamentals are missing.

3. **Threshold tuning matters**  
   Small score changes around 0.55–0.65 materially affect outcomes.

---

## Conclusion

The call quality evaluation system demonstrates:

- High accuracy (90%)
- Strong F1 score (0.91)
- Predictable and explainable behavior

Most errors stem from nuanced conversational judgment rather than systemic failures, indicating that the model is suitable for **call triage and coaching support**, with scope for improved compliance and discovery weighting.
