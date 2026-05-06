import json


def analyze_interaction(interaction_data):

    narrative = interaction_data.get("narrative", "").lower()

    analysis_result = {
        "themes": [],
        "emotional_signals": [],
        "dynamics_classification": "",
        "organizational_signals": [],
        "governance_recommendations": []
    }

    # Theme Detection
    if "policy" in narrative or "discussion" in narrative:
        analysis_result["themes"].append("participation")

    if "fatigue" in narrative or "overload" in narrative:
        analysis_result["themes"].append("burnout")

    if "collaboration" in narrative:
        analysis_result["themes"].append("innovation")

    # Emotional Signal Detection
    if "questioned" in narrative:
        analysis_result["emotional_signals"].append("critical_reflection")

    if "fatigue" in narrative:
        analysis_result["emotional_signals"].append("fatigue")

    if "proposed" in narrative:
        analysis_result["emotional_signals"].append("optimism")

    # Dynamics Classification
    if "questioned" in narrative:
        analysis_result["dynamics_classification"] = "constructive_divergence"

    elif "fatigue" in narrative:
        analysis_result["dynamics_classification"] = "destructive_divergence"

    elif "collaboration" in narrative:
        analysis_result["dynamics_classification"] = "positive_convergence"

    else:
        analysis_result["dynamics_classification"] = "neutral"

    # Organizational Signals
    if "participation" in analysis_result["themes"]:
        analysis_result["organizational_signals"].append(
            "participation_gap_signal"
        )

    if "burnout" in analysis_result["themes"]:
        analysis_result["organizational_signals"].append(
            "burnout_signal"
        )

    if "innovation" in analysis_result["themes"]:
        analysis_result["organizational_signals"].append(
            "innovation_signal"
        )

    # Governance Recommendations
    if analysis_result["dynamics_classification"] == "constructive_divergence":
        analysis_result["governance_recommendations"].append(
            "increase participatory dialogue"
        )

    if analysis_result["dynamics_classification"] == "destructive_divergence":
        analysis_result["governance_recommendations"].append(
            "review workload and reduce administrative pressure"
        )

    if analysis_result["dynamics_classification"] == "positive_convergence":
        analysis_result["governance_recommendations"].append(
            "support collaborative initiatives"
        )

    return analysis_result


if __name__ == "__main__":

    sample_input = {
        "narrative": "Senior lecturer questioned why policy discussions were not initiated through lecturer discussions."
    }

    result = analyze_interaction(sample_input)

    print(json.dumps(result, indent=2))
