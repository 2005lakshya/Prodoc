from typing import Dict, List

# Core pipeline imports
from src.prodoc_pipeline import (
    split_clauses,
    normalize_clauses,
    classify_clauses,
    detect_risks,
    aggregate_risk,
    classify_decision,
    generate_summary
)

from src.critical_clauses import CRITICAL_CLAUSE_TYPES
from src.risk_thresholds import CONFIDENCE_THRESHOLDS


# -------------------------------------------------
# Helper: Clause Structural Strength
# -------------------------------------------------
def is_structurally_strong_clause(clause_text: str) -> bool:
    """
    Determines whether a clause appears legally complete and balanced.
    Used to avoid penalizing well-written clauses with low ML confidence.
    """
    words = clause_text.split()

    # Long clauses are usually real
    if len(words) >= 60:
        return True

    strong_keywords = [
        "each party",
        "either party",
        "shall",
        "may",
        "governed by",
        "indemnify",
        "termination",
        "terminate",
        "liability",
        "confidential"
    ]

    hits = sum(1 for k in strong_keywords if k in clause_text.lower())
    return hits >= 2


# -------------------------------------------------
# Helper: Contract Complexity
# -------------------------------------------------
def is_complex_contract(contract_text: str) -> bool:
    """
    Determines if a contract is large/complex (e.g., government or enterprise).
    """
    word_count = len(contract_text.split())
    return word_count > 1200


# -------------------------------------------------
# Main PRODOC Service
# -------------------------------------------------
def run_prodoc_on_text(contract_text: str, contract_title: str) -> Dict:
    """
    Runs the full PRODOC pipeline and returns frontend-ready JSON.
    """

    # 1. Split and normalize clauses
    raw_clauses = split_clauses(contract_text)
    clauses = normalize_clauses(raw_clauses)

    # 2. Classify clauses
    clauses = classify_clauses(clauses)

    # 3. Detect risks (raw)
    detected_risks = detect_risks(clauses)

    # 4. Aggregate risks
    risk_score, breakdown = aggregate_risk(detected_risks)

    # -------------------------------------------------
    # 5. Build highlight evidence (USER-VISIBLE RISKS)
    # -------------------------------------------------
    highlights: List[Dict] = []

    for clause in clauses:
        if clause["label"] not in CRITICAL_CLAUSE_TYPES:
            continue

        # Skip strong clauses
        if is_structurally_strong_clause(clause["text"]):
            continue

        # Highlight only genuinely weak / uncertain clauses
        if clause["confidence"] < CONFIDENCE_THRESHOLDS["LOW"]:
            highlights.append({
                "clause_id": clause["clause_id"],
                "risk_type": "LOW_CONFIDENCE_CRITICAL_CLAUSE",
                "label": clause["label"],
                "confidence": round(clause["confidence"], 3),
                "text": clause["text"][:600]
            })

    # -------------------------------------------------
    # 6. FINAL DECISION LOGIC (CRITICAL)
    # -------------------------------------------------
    if len(highlights) == 0:
        # No actionable risks detected
        if is_complex_contract(contract_text):
            decision = "REQUIRES_LEGAL_REVIEW"
            summary = (
                "No critical risk signals detected. "
                "However, due to the length and complexity of the contract, "
                "a legal review is recommended."
            )
        elif risk_score <= 5:
            decision = "SAFE_TO_SIGN"
            summary = (
                "No significant legal risks detected. "
                "Contract appears balanced and safe to proceed."
            )
        else:
            decision = "REQUIRES_LEGAL_REVIEW"
            summary = (
                "Minor uncertainties detected. "
                "A brief legal review is recommended before approval."
            )
    else:
        # Evidence-backed risk exists
        decision = classify_decision(risk_score)
        summary = generate_summary(decision, breakdown)

    # -------------------------------------------------
    # 7. Final API Response
    # -------------------------------------------------
    return {
        "contract_title": contract_title,
        "decision": decision,
        "risk_score": round(risk_score, 2),
        "highlights": highlights,
        "justification_report": summary
    }
