import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "contracts" / "CUAD_v1.json"

def load_cuad():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    if not DATA_PATH.is_file():
        raise IsADirectoryError(f"Expected a file but found a directory at {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

if __name__ == "__main__":
    cuad_data = load_cuad()

    print("CUAD loaded successfully")
    print("Total contracts:", len(cuad_data["data"]))

    first_contract = cuad_data["data"][0]
    print("\nContract title:")
    print(first_contract["title"])

    first_text = first_contract["paragraphs"][0]["context"]
    print("\nContract text preview:\n")
    print(first_text[:500])
