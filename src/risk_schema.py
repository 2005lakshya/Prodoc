from typing import Dict, List

RISK_SIGNALS = [
    {
        "id": "MISSING_CRITICAL_CLAUSE",
        "description": "A critical legal clause is missing from the contract",
        "severity": "HIGH"
    },
    {
        "id": "LOW_CONFIDENCE_CRITICAL_CLAUSE",
        "description": "A critical clause exists but was extracted or classified with low confidence",
        "severity": "MEDIUM"
    },
    {
        "id": "ONE_SIDED_OBLIGATION",
        "description": "Obligations appear to be heavily skewed toward one party",
        "severity": "HIGH"
    },
    {
        "id": "LONG_TERM_COMMITMENT",
        "description": "The contract term is unusually long or restrictive",
        "severity": "MEDIUM"
    },
    {
        "id": "WEAK_TERMINATION_RIGHTS",
        "description": "Termination rights are missing or unfavorable",
        "severity": "HIGH"
    },
    {
        "id": "AMBIGUOUS_GRANT",
        "description": "License or grant language is broad or unclear",
        "severity": "MEDIUM"
    }
]
