import streamlit as st
import json
import os
import pandas as pd
from itertools import combinations
from datetime import datetime
DATASET_DIR = "../datasets/structured-interactions"
actor_frequency = {}
actor_connections = {}
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

        for pair in combinations(sorted(actors), 2):
            actor_connections[pair] = actor_connections.get(pair, 0) + 1

        pulse_data = data.get("pulse_impact", {})
        timestamp = data.get("timestamp", "Unknown")

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

st.subheader("Input Governance Interaction")

with st.form("interaction_form"):

    interaction_type = st.selectbox(
        "Interaction Type",
        [
            "policy_discussion",
            "innovation_meeting",
            "student_feedback",
            "organizational_conflict",
            "curriculum_review"
        ]
    )

    actors_input = st.text_input(
        "Actors (pisahkan dengan koma)",
        "lecturer, student"
    )

    narrative = st.text_area(
        "Narrative",
        "Describe the governance interaction..."
    )

    trust_pulse = st.slider("Trust Pulse", -5, 5, 0)

    participation_pulse = st.slider(
        "Participation Pulse",
        -5,
        5,
        0
    )

    innovation_pulse = st.slider(
        "Innovation Pulse",
        -5,
        5,
        0
    )

    submitted = st.form_submit_button(
        "Save Interaction"
    )
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
st.divider()

st.subheader("Governance Heatmap")

for key, value in pulse_totals.items():

    if value <= -5:
        color = "🔴 CRITICAL"

    elif value < 0:
        color = "🟡 WARNING"

    else:
        color = "🟢 STABLE"

    st.markdown(f"### {key}")
    st.progress((value + 10) / 20)

    st.write(f"Status: {color} ({value})")
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

actor_df = actor_df.sort_values(by="Frequency", ascending=True)

st.bar_chart(
    actor_df.set_index("Actor"),
    horizontal=True
)
st.divider()

st.subheader("Early Warning System")

if pulse_totals["trust_pulse"] <= -10:
    st.error("⚠️ Institutional Trust Collapse Risk")

if pulse_totals["participation_pulse"] <= -10:
    st.warning("⚠️ Participation Crisis Emerging")

if pulse_totals["innovation_pulse"] <= -10:
    st.warning("⚠️ Innovation Stagnation Risk")

if pulse_totals["fatigue_pulse"] >= 8:
    st.error("⚠️ Organizational Fatigue Critical")

if pulse_totals["coordination_pulse"] <= -8:
    st.warning("⚠️ Coordination Breakdown Detected")

if (
    pulse_totals["trust_pulse"] > -10
    and pulse_totals["participation_pulse"] > -10
    and pulse_totals["innovation_pulse"] > -10
):
    st.success("✅ No major institutional governance threats detected.")
st.divider()

st.subheader("Governance Network Map")

connection_data = []

for pair, weight in actor_connections.items():

    connection_data.append({
        "Actor Pair": f"{pair[0]} ↔ {pair[1]}",
        "Frequency": weight
    })

connection_df = pd.DataFrame(connection_data)

if not connection_df.empty:

    top_connections = connection_df.sort_values(
        by="Frequency",
        ascending=False
    ).head(15)

    st.dataframe(top_connections)
