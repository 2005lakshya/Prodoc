from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_NAME = "nlpaueb/legal-bert-base-uncased"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        force_download=True
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        force_download=True,
        num_labels=8,
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
    predicted_class = torch.argmax(logits, dim=1).item()

    return predicted_class, logits

if __name__ == "__main__":
    sample_clause = (
        "The Company hereby grants the Distributor the exclusive right "
        "to sell and distribute the Products within the Market."
    )

    tokenizer, model = load_model()
    pred_class, logits = classify_clause(sample_clause, tokenizer, model)

    print("Sample clause:")
    print(sample_clause)
    print("\nPredicted class index:", pred_class)
    print("Raw logits:", logits)
