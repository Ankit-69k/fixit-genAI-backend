# Lead Prioritisation Evaluation

## Objective

Evaluate the effectiveness of the **Lead Prioritization API** by comparing model predictions against manually labeled ground truth for a small, representative subset of leads.

The goal is not absolute accuracy, but to assess:

- ranking quality
- score–bucket consistency
- strengths and failure modes

---

## Dataset Selection

From the full `leads.csv`, **20 leads** were selected to ensure diversity across:

- budget ranges
- activity recency
- interaction counts
- lead sources
- note quality

## Ground Truth Labeling

Each lead was **manually labeled** based on human judgment considering:

- buying urgency
- recency
- engagement depth
- intent in notes

### Ground Truth Distribution

| Bucket | Count |
| ------ | ----- |
| Hot    | 7     |
| Warm   | 8     |
| Cold   | 5     |

---

## Model Predictions

The 20 leads were passed through:

```
POST /api/v1/lead-priority
```

The API returned a `priority_score` (0–1) and a `priority_bucket`.

### Prediction Summary

| Bucket | Predicted Count |
| ------ | --------------- |
| Hot    | 8               |
| Warm   | 7               |
| Cold   | 5               |

---

## Metrics

### 1️⃣ Precision & Recall (Hot Leads)

Hot leads were treated as the **positive class**.

- **True Positives (TP):** 6
- **False Positives (FP):** 2
- **False Negatives (FN):** 1

#### Precision (Hot)

```
Precision = TP / (TP + FP) = 6 / 8 = 0.75
```

#### Recall (Hot)

```
Recall = TP / (TP + FN) = 6 / 7 ≈ 0.86
```

**Interpretation:**  
The system is better at **capturing most hot leads (high recall)** than avoiding false positives.

---

### 2️⃣ Correlation Between Score and Bucket

Buckets were mapped numerically:

- Cold = 1
- Warm = 2
- Hot = 3

A **Spearman rank correlation** was computed between:

- `priority_score`
- mapped bucket value

**Result:**

```
Spearman correlation ≈ 0.82
```

This indicates a **strong monotonic relationship** between score and bucket assignment.

---

## Key Insights

### Insight 1: Strong Recall Driven by LLM Intent

Leads with **strong buying language in notes** were consistently promoted to _hot_, even when some structured signals (e.g., moderate activity delay) were weaker.  
This significantly improved recall for hot leads.

---

### Insight 2: False Positives from High Budget Bias

Some high-budget leads with **older activity** were still classified as hot.  
This suggests the deterministic budget rule slightly overweights monetary value compared to recency decay.

---

### Insight 3: Buckets Are Internally Consistent

The high score–bucket correlation shows that:

- scores are not arbitrary
- bucket thresholds align well with numeric ranking  
  This makes the system predictable and explainable.

---

## Limitations

- Small evaluation set (20 leads)
- Manual labeling introduces subjectivity
- No temporal validation (single snapshot)

---

## Conclusion

The lead prioritization system demonstrates:

- **High recall for hot leads**
- **Strong internal consistency**
- **Explainable behavior from combined rules + LLM signals**

The evaluation confirms the system is suitable for **ranking and triage**, with clear areas identified for future tuning.
