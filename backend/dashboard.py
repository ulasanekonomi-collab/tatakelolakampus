import json
import os

DATASET_FOLDER = "../datasets/structured-interactions"

pulse_totals = {
    "trust_pulse": 0,
    "participation_pulse": 0,
    "innovation_pulse": 0,
    "fatigue_pulse": 0,
    "coordination_pulse": 0
}

for filename in os.listdir(DATASET_FOLDER):

    if filename.endswith(".json"):

        filepath = os.path.join(DATASET_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            pulse = data.get("pulse_impact", {})

            for key in pulse_totals:
                pulse_totals[key] += pulse.get(key, 0)

print("\n=== INSTITUTIONAL GOVERNANCE DASHBOARD ===\n")

for key, value in pulse_totals.items():
    print(f"{key}: {value}")
