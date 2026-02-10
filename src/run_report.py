import json
from generate_report import generate_decision_report
from prodoc_pipeline import load_cuad

if __name__ == "__main__":
    from prodoc_pipeline import (
        extract_full_contract_text,
        split_clauses,
        normalize_clauses,
        classify_clauses,
        detect_risks,
        aggregate_risk,
        classify_decision,
        generate_summary
    )

    cuad = load_cuad()
    contract = cuad["data"][0]

    text = extract_full_contract_text(contract)
    raw = split_clauses(text)
    clauses = normalize_clauses(raw)
    clauses = classify_clauses(clauses)

    detected_risks = detect_risks(clauses)
    score, breakdown = aggregate_risk(detected_risks)
    decision = classify_decision(score)
    summary = generate_summary(decision, breakdown)

    pipeline_output = {
        "contract_title": contract["title"],
        "decision": decision,
        "risk_score": score,
        "risks": breakdown,
        "summary": summary
    }

    report = generate_decision_report(pipeline_output)
    print(report)
    