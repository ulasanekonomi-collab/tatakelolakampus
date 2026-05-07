import streamlit as st
import json
import os

DATASET_DIR = "../datasets/structured-interactions"

pulse_totals = {
    "trust_pulse": 0,
    "participation_pulse": 0,
    "innovation_pulse": 0,
    "fatigue_pulse": 0,
    "coordination_pulse": 0
}

interaction_count = 0

for filename in os.listdir(DATASET_DIR):
    if filename.endswith(".json"):

        filepath = os.path.join(DATASET_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        pulse_data = data.get("pulse_index", {})

        for key in pulse_totals:
            pulse_totals[key] += pulse_data.get(key, 0)

        interaction_count += 1

st.title("TatakelolaKampus")
st.subheader("Institutional Governance Dashboard")

st.metric("Total Interactions", interaction_count)

st.divider()

for key, value in pulse_totals.items():
    st.metric(key, value)
