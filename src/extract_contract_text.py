import json
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

if __name__ == "__main__":
    cuad_data = load_cuad()

    contract = cuad_data["data"][0]
    contract_text = extract_full_contract_text(contract)

    print("Contract title:")
    print(contract["title"])
    print("\nFull contract text preview (first 1500 characters):\n")
    print(contract_text[:1500])
