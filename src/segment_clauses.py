import json
import re
from pathlib import Path

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

def basic_clause_split(text):
    """
    Split contract text using common legal clause patterns:
    - Section numbers (e.g., '1.', '2.1', 'ARTICLE IV')
    - Capitalized headings
    """

    pattern = r"\n\s*(?=(ARTICLE\s+[IVXLC]+|\d+\.\d+|\d+\.)\s+)"

    clauses = re.split(pattern, text, flags=re.IGNORECASE)

    cleaned_clauses = []
    for c in clauses:
        c = c.strip()
        if len(c) > 200:
            cleaned_clauses.append(c)

    return cleaned_clauses

if __name__ == "__main__":
    cuad_data = load_cuad()
    contract = cuad_data["data"][0]

    full_text = extract_full_contract_text(contract)
    clauses = basic_clause_split(full_text)

    print("Contract title:")
    print(contract["title"])
    print("\nTotal clauses detected:", len(clauses))

    print("\nFirst 3 clauses:\n")
    for i, clause in enumerate(clauses[:3], start=1):
        print(f"--- Clause {i} ---")
        print(clause[:800])
        print()
