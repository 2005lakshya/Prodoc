import json
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from clause_schema import CLAUSE_LABELS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "contracts" / "CUAD_v1.json"

MODEL_NAME = "nlpaueb/legal-bert-base-uncased"

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
    normalized = []
    for i, text in enumerate(clauses, start=1):
        normalized.append({
            "clause_id": f"CL-{i:03d}",
            "order": i,
            "text": text
        })
    return normalized

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(CLAUSE_LABELS),
        ignore_mismatched_sizes=True
    )
    model.eval()
    return tokenizer, model

def classify_clause(text, tokenizer, model):
    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    pred_idx = torch.argmax(logits, dim=1).item()
    confidence = torch.softmax(logits, dim=1)[0][pred_idx].item()
    return pred_idx, confidence

if __name__ == "__main__":
    cuad = load_cuad()
    contract = cuad["data"][0]

    full_text = extract_full_contract_text(contract)
    raw_clauses = basic_clause_split(full_text)
    clauses = normalize_clauses(raw_clauses)

    tokenizer, model = load_model()

    print("Contract title:")
    print(contract["title"])
    print()

    for clause in clauses[:5]:
        label_idx, confidence = classify_clause(clause["text"], tokenizer, model)
        label = CLAUSE_LABELS.get(label_idx, "Unknown")

        clause["label"] = label
        clause["confidence"] = round(confidence, 3)

        print(f"{clause['clause_id']} | {label} | confidence={clause['confidence']}")
        print(clause["text"][:400])
        print("-" * 80)
