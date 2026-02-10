def generate_decision_report(pipeline_output):
    """
    pipeline_output: dict produced by prodoc_pipeline
    """

    decision = pipeline_output["decision"]
    score = pipeline_output["risk_score"]
    risks = pipeline_output["risks"]
    summary = pipeline_output["summary"]
    title = pipeline_output["contract_title"]

    report_lines = []

    # 1. Decision Summary
    report_lines.append("DECISION JUSTIFICATION REPORT")
    report_lines.append("=" * 30)
    report_lines.append(f"Contract: {title}")
    report_lines.append(f"Final Decision: {decision}")
    report_lines.append("")

    # 2. Risk Score Explanation
    report_lines.append("1. Risk Score Overview")
    report_lines.append("-" * 25)
    report_lines.append(
        f"The contract received a total risk score of {score}. "
        "This score is calculated by aggregating individual legal risk signals "
        "identified during automated analysis."
    )
    report_lines.append("")

    # 3. Key Risk Factors
    report_lines.append("2. Key Risk Factors")
    report_lines.append("-" * 25)

    if not risks:
        report_lines.append("No significant legal risk factors were identified.")
    else:
        for r in risks:
            report_lines.append(
                f"- Risk Type: {r['risk_id']}, "
                f"Occurrences: {r['count']}, "
                f"Risk Contribution: {r['contribution']}"
            )

    report_lines.append("")

    # 4. Evidence References
    report_lines.append("3. Evidence and Traceability")
    report_lines.append("-" * 25)
    report_lines.append(
        "Each risk listed above is traceable to specific contract clauses "
        "and was identified using a combination of clause classification, "
        "confidence assessment, and rule-based legal reasoning."
    )
    report_lines.append("")

    # 5. Recommended Actions
    report_lines.append("4. Recommended Next Actions")
    report_lines.append("-" * 25)

    if decision == "SAFE_TO_SIGN":
        report_lines.append(
            "No immediate legal action is required. The contract appears "
            "suitable for approval based on automated analysis."
        )
    elif decision == "REQUIRES_LEGAL_REVIEW":
        report_lines.append(
            "The contract should be reviewed by a legal professional to "
            "address the identified risks before approval."
        )
    else:
        report_lines.append(
            "The contract presents high legal risk. Approval is not "
            "recommended without significant legal review and remediation."
        )

    report_lines.append("")
    report_lines.append("Note: This report is AI-assisted and intended to support, "
                        "not replace, human decision-making.")

    return "\n".join(report_lines)
