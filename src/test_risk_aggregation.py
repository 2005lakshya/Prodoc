from aggregate_risk import aggregate_risk, classify_decision

if __name__ == "__main__":
    detected_risks = [
        {"id": "MISSING_CRITICAL_CLAUSE", "count": 4},
        {"id": "LOW_CONFIDENCE_CRITICAL_CLAUSE", "count": 6},
        {"id": "ONE_SIDED_OBLIGATION", "count": 0},
        {"id": "WEAK_TERMINATION_RIGHTS", "count": 0}
    ]

    score, breakdown = aggregate_risk(detected_risks)
    decision = classify_decision(score)

    print("Final risk score:", score)
    print("Decision:", decision)
    print("\nBreakdown:")
    for b in breakdown:
        print(b)
