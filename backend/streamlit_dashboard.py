import streamlit as st
st.title("dikembangkan oleh Yuhka Sundaya")
import json
import os
import pandas as pd

DATASET_DIR = "../datasets/structured-interactions"
actor_frequency = {}
pulse_totals = {
    "trust_pulse": 0,
    "participation_pulse": 0,
    "innovation_pulse": 0,
    "fatigue_pulse": 0,
    "coordination_pulse": 0
}

interaction_count = 0

timeline_data = []
for filename in os.listdir(DATASET_DIR):
    if filename.endswith(".json"):

        filepath = os.path.join(DATASET_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
actors = data.get("actors", [])

for actor in actors:
    actor_frequency[actor] = actor_frequency.get(actor, 0) + 1            
        #st.write(data)

        pulse_data = data.get("pulse_impact", {})
        timestamp = data.get("timestamp", "Unknown")
#        st.write(pulse_data)

        for key in pulse_totals:
            pulse_totals[key] += pulse_data.get(key, 0)
timeline_data.append({
    "timestamp": timestamp,
    "trust_pulse": pulse_data.get("trust_pulse", 0),
    "participation_pulse": pulse_data.get("participation_pulse", 0),
    "innovation_pulse": pulse_data.get("innovation_pulse", 0),
})

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
st.divider()

st.subheader("Institutional Pulse Timeline")

timeline_df = pd.DataFrame(timeline_data)

timeline_df = timeline_df.sort_values("timestamp")

st.line_chart(
    timeline_df.set_index("timestamp")[
        ["trust_pulse", "participation_pulse", "innovation_pulse"]
    ]
)
st.divider()

st.subheader("AI Institutional Interpretation")

if pulse_totals["trust_pulse"] <= -5:
    st.error(
        "Trust institutional climate is deteriorating. Internal legitimacy and confidence are weakening."
    )

if pulse_totals["participation_pulse"] <= -5:
    st.warning(
        "Participation deficit detected. Institutional actors may feel excluded from governance processes."
    )

if pulse_totals["innovation_pulse"] <= -5:
    st.warning(
        "Innovation stagnation detected. Organizational creativity and adaptive capacity are declining."
    )

if (
    pulse_totals["trust_pulse"] >= 0
    and pulse_totals["participation_pulse"] >= 0
):
    st.success(
        "Institutional governance climate remains relatively stable and collaborative."
    )
st.divider()

st.subheader("Institutional Health Score")

health_score = 100 + (
    pulse_totals["trust_pulse"]
    + pulse_totals["participation_pulse"]
    + pulse_totals["innovation_pulse"]
    + pulse_totals["coordination_pulse"]
    - abs(pulse_totals["fatigue_pulse"])
)

health_score = max(0, min(100, health_score))

st.metric("Institutional Health", f"{health_score}/100")
st.divider()

st.subheader("Institutional Risk Level")

if health_score >= 85:
    st.success("LOW RISK — Institutional governance is healthy and adaptive.")

elif health_score >= 70:
    st.warning("MODERATE RISK — Some governance tensions require attention.")

else:
    st.error("HIGH RISK — Institutional instability indicators are escalating.")
st.divider()

st.subheader("Institutional Actor Activity")

actor_df = pd.DataFrame({
    "Actor": list(actor_frequency.keys()),
    "Frequency": list(actor_frequency.values())
})

st.bar_chart(actor_df.set_index("Actor"))
