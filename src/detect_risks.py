import json
from pathlib import Path

from clause_schema import CLAUSE_LABELS
from critical_clauses import CRITICAL_CLAUSE_TYPES
from risk_thresholds import CONFIDENCE_THRESHOLDS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "contracts" / "CUAD_v1.json"

def load_cuad():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_full_contract_text(contract):
    paragraphs = contract["paragraphs"]
    texts = []
    for p in paragraphs:
        t = p.get("context", "").strip()
        if t:
            texts.append(t)
    return "\n\n".join(texts)

def basic_clause_split(text):
    import re
    pattern = r"\n\s*(?=(ARTICLE\s+[IVXLC]+|\d+\.\d+|\d+\.)\s+)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p and len(p.strip()) > 200]

def normalize_clauses(clauses):
    return [
        {
            "clause_id": f"CL-{i:03d}",
            "order": i,
            "text": text
        }
        for i, text in enumerate(clauses, start=1)
    ]

def load_classified_clauses(contract):
    """
    For now, we re-run classification inline.
    Later, this will be refactored into a pipeline.
    """
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    MODEL_NAME = "nlpaueb/legal-bert-base-uncased"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(CLAUSE_LABELS),
        ignore_mismatched_sizes=True
    )
    model.eval()

    full_text = extract_full_contract_text(contract)
    raw = basic_clause_split(full_text)
    clauses = normalize_clauses(raw)

    for clause in clauses:
        inputs = tokenizer(
            clause["text"],
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        idx = logits.argmax(dim=1).item()
        confidence = logits.softmax(dim=1)[0][idx].item()

        clause["label"] = CLAUSE_LABELS.get(idx, "Unknown")
        clause["confidence"] = confidence

    return clauses

def detect_missing_critical_clauses(clauses):
    present_types = {c["label"] for c in clauses}
    missing = CRITICAL_CLAUSE_TYPES - present_types
    return missing

def detect_low_confidence_critical_clauses(clauses):
    low_conf = []
    for c in clauses:
        if (
            c["label"] in CRITICAL_CLAUSE_TYPES
            and c["confidence"] < CONFIDENCE_THRESHOLDS["LOW"]
        ):
            low_conf.append(c)
    return low_conf

from obligation_heuristics import (
    OBLIGATION_KEYWORDS,
    ONE_SIDED_PARTY_TERMS,
    COUNTERPARTY_TERMS,
    TERMINATION_KEYWORDS
)

def detect_one_sided_obligations(clauses):
    risky_clauses = []

    for c in clauses:
        text = c["text"].lower()

        obligation_hits = sum(
            1 for k in OBLIGATION_KEYWORDS if k in text
        )

        one_sided_hits = sum(
            1 for p in ONE_SIDED_PARTY_TERMS if p.lower() in text
        )

        counterparty_hits = sum(
            1 for p in COUNTERPARTY_TERMS if p.lower() in text
        )

        if obligation_hits >= 2 and one_sided_hits > counterparty_hits:
            risky_clauses.append(c)

    return risky_clauses


def detect_weak_termination_rights(clauses):
    termination_clauses = [
        c for c in clauses
        if c["label"] == "Termination"
        or any(k in c["text"].lower() for k in TERMINATION_KEYWORDS)
    ]

    if not termination_clauses:
        return "NO_TERMINATION_CLAUSE"

    weak = []
    for c in termination_clauses:
        text = c["text"].lower()
        if "only" in text or "sole discretion" in text:
            weak.append(c)

    return weak

if __name__ == "__main__":
    cuad = load_cuad()
    contract = cuad["data"][0]

    clauses = load_classified_clauses(contract)

    missing = detect_missing_critical_clauses(clauses)
    low_conf = detect_low_confidence_critical_clauses(clauses)

    print("Contract title:")
    print(contract["title"])
    print()

    if missing:
        print("RISK: Missing critical clauses:")
        for m in missing:
            print("-", m)
    else:
        print("No missing critical clauses detected.")

    print()

    if low_conf:
        print("RISK: Low-confidence critical clauses:")
        for c in low_conf:
            print(
                f"{c['clause_id']} | {c['label']} | confidence={round(c['confidence'], 3)}"
            )
    else:
        print("No low-confidence critical clauses detected.")

    one_sided = detect_one_sided_obligations(clauses)
    termination_issues = detect_weak_termination_rights(clauses)

    print()

    if one_sided:
        print("RISK: One-sided obligations detected in clauses:")
        for c in one_sided:
            print(f"{c['clause_id']} | {c['label']}")
    else:
        print("No obvious one-sided obligations detected.")

    print()

    if termination_issues == "NO_TERMINATION_CLAUSE":
        print("RISK: No termination clause detected.")
    elif termination_issues:
        print("RISK: Weak termination rights detected in clauses:")
        for c in termination_issues:
            print(f"{c['clause_id']} | {c['label']}")
    else:
        print("Termination rights appear present.")
