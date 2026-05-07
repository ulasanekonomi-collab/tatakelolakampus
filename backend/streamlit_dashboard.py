import streamlit as st
st.title("dikembangkan oleh Yuhka Sundaya")
import json
import os
import pandas as pd

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
            
        #st.write(data)

        pulse_data = data.get("pulse_impact", {})
#        st.write(pulse_data)

        for key in pulse_totals:
            pulse_totals[key] += pulse_data.get(key, 0)

        interaction_count += 1

st.title("TatakelolaKampus")
st.subheader("Institutional Governance Dashboard")
for key, value in pulse_totals.items():

    if value <= -5:
        st.error(f"{key}: CRITICAL ({value})")

    elif value < 0:
        st.warning(f"{key}: WARNING ({value})")

    else:
        st.success(f"{key}: STABLE ({value})")
st.metric("Total Interactions", interaction_count)

st.divider()

for key, value in pulse_totals.items():
    st.metric(key, value)
st.divider()

st.subheader("Institutional Pulse Overview")

pulse_df = pd.DataFrame({
    "Pulse": list(pulse_totals.keys()),
    "Score": list(pulse_totals.values())
})

st.bar_chart(pulse_df.set_index("Pulse"))
