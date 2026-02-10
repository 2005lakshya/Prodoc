import json
from pathlib import Path

from src.clause_schema import CLAUSE_LABELS
from src.critical_clauses import CRITICAL_CLAUSE_TYPES
from src.risk_thresholds import CONFIDENCE_THRESHOLDS
from src.risk_weights import RISK_WEIGHTS
from src.decision_thresholds import DECISION_THRESHOLDS
from src.aggregate_risk import aggregate_risk, classify_decision


from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "contracts" / "CUAD_v1.json"

MODEL_NAME = "nlpaueb/legal-bert-base-uncased"


def load_cuad():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_full_contract_text(contract):
    texts = []
    for p in contract["paragraphs"]:
        t = p.get("context", "").strip()
        if t:
            texts.append(t)
    return "\n\n".join(texts)


def split_clauses(text):
    pattern = r"\n\s*(?=(ARTICLE\s+[IVXLC]+|\d+\.\d+|\d+\.)\s+)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p and len(p.strip()) > 200]


def normalize_clauses(raw_clauses):
    return [
        {"clause_id": f"CL-{i:03d}", "text": txt}
        for i, txt in enumerate(raw_clauses, start=1)
    ]


def classify_clauses(clauses):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(CLAUSE_LABELS),
        ignore_mismatched_sizes=True
    )
    model.eval()

    for c in clauses:
        inputs = tokenizer(
            c["text"],
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        idx = logits.argmax(dim=1).item()
        confidence = logits.softmax(dim=1)[0][idx].item()

        c["label"] = CLAUSE_LABELS.get(idx, "Unknown")
        c["confidence"] = confidence

    return clauses

def is_structurally_strong_clause(clause_text: str) -> bool:
    words = clause_text.split()

    if len(words) >= 60:
        return True

    strong_keywords = [
        "each party",
        "either party",
        "shall",
        "may",
        "governed by",
        "indemnify",
        "terminate",
        "liability"
    ]

    hits = sum(1 for k in strong_keywords if k in clause_text.lower())
    return hits >= 2

def detect_risks(clauses):
    risks = []

    present_types = {c["label"] for c in clauses}
    missing = CRITICAL_CLAUSE_TYPES - present_types
    if missing:
        risks.append({
            "id": "MISSING_CRITICAL_CLAUSE",
            "count": len(missing)
        })

    low_conf = [
    c for c in clauses
    if c["label"] in CRITICAL_CLAUSE_TYPES
    and c["confidence"] < CONFIDENCE_THRESHOLDS["LOW"]
    and not is_structurally_strong_clause(c["text"])
]


    if low_conf:
        risks.append({
            "id": "LOW_CONFIDENCE_CRITICAL_CLAUSE",
            "count": len(low_conf)
        })

    return risks


def generate_summary(decision, breakdown):
    if decision == "SAFE_TO_SIGN":
        return "No significant legal risks detected. Contract appears safe to proceed."
    if decision == "REQUIRES_LEGAL_REVIEW":
        return "Contract contains legal risks that require human legal review."
    return "Contract presents high legal risk due to missing or unreliable critical clauses."


if __name__ == "__main__":
    cuad = load_cuad()
    contract = cuad["data"][0]

    text = extract_full_contract_text(contract)
    raw_clauses = split_clauses(text)
    clauses = normalize_clauses(raw_clauses)
    clauses = classify_clauses(clauses)

    detected_risks = detect_risks(clauses)
    score, breakdown = aggregate_risk(detected_risks)
    decision = classify_decision(score)
    summary = generate_summary(decision, breakdown)

    output = {
        "contract_title": contract["title"],
        "decision": decision,
        "risk_score": score,
        "risks": breakdown,
        "summary": summary
    }

    print(json.dumps(output, indent=2))
