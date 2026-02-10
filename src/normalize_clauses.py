import json
import re
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "contracts" / "CUAD_v1.json"

def load_cuad():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_full_contract_text(contract):
    paragraphs = contract["paragraphs"]
    full_text = []

    for p in paragraphs:
        text = p.get("context", "").strip()
        if text:
            full_text.append(text)

    return "\n\n".join(full_text)

def basic_clause_split(text: str) -> List[str]:
    pattern = r"\n\s*(?=(ARTICLE\s+[IVXLC]+|\d+\.\d+|\d+\.)\s+)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    clauses = []
    for p in parts:
        p = p.strip()
        if len(p) > 200:
            clauses.append(p)

    return clauses

def normalize_clauses(clauses: List[str]) -> List[Dict]:
    normalized = []

    for idx, clause_text in enumerate(clauses, start=1):
        clause = {
            "clause_id": f"CL-{idx:03d}",
            "order": idx,
            "text": clause_text
        }
        normalized.append(clause)

    return normalized

if __name__ == "__main__":
    cuad_data = load_cuad()
    contract = cuad_data["data"][0]

    full_text = extract_full_contract_text(contract)
    raw_clauses = basic_clause_split(full_text)
    clauses = normalize_clauses(raw_clauses)

    print("Contract title:")
    print(contract["title"])
    print("\nTotal normalized clauses:", len(clauses))

    print("\nFirst 3 normalized clauses:\n")
    for c in clauses[:3]:
        print(f"Clause ID: {c['clause_id']}")
        print(f"Order: {c['order']}")
        print(c["text"][:600])
        print()
