from src.risk_weights import RISK_WEIGHTS
from src.decision_thresholds import DECISION_THRESHOLDS
def aggregate_risk(detected_risks):
    """
    detected_risks: list of dicts
    Each dict must have:
      - id: risk id string
      - count: number of occurrences
    """

    total_score = 0.0
    breakdown = []

    for risk in detected_risks:
        risk_id = risk["id"]
        count = risk.get("count", 1)

        weight = RISK_WEIGHTS.get(risk_id, 0.0)
        contribution = weight * count

        total_score += contribution

        breakdown.append({
            "risk_id": risk_id,
            "count": count,
            "weight": weight,
            "contribution": contribution
        })

    return round(total_score, 2), breakdown

def classify_decision(total_score):
    if total_score >= DECISION_THRESHOLDS["HIGH_RISK"]:
        return "HIGH_RISK"
    elif total_score >= DECISION_THRESHOLDS["REQUIRES_REVIEW"]:
        return "REQUIRES_LEGAL_REVIEW"
    else:
        return "SAFE_TO_SIGN"
