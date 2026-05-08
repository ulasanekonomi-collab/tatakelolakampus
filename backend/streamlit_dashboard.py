import streamlit as st
import json
import os
import pandas as pd
from itertools import combinations
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="TatakelolaKampus",
    layout="wide"
)

DATASET_DIR = "datasets/structured-interactions"

# =========================================================
# DATA CONTAINER
# =========================================================

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

# =========================================================
# LOAD DATASET
# =========================================================

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

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

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([1,4])

with col1:
    st.image("assets/Yuhka-Sundaya.png", width=120)

with col2:
    st.title("Campus Governance Intelligence")
    st.caption(
        "Developed by Yuhka Sundaya · Ekonomi Pembangunan UNISBA"
    )

# =========================================================
# MAIN LAYOUT
# =========================================================

left_col, middle_col, right_col = st.columns([2,1,1])

# =========================================================
# LEFT PANEL — INPUT
# =========================================================

with left_col:

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

        trust_pulse = st.slider(
            "Trust Pulse",
            -5,
            5,
            0
        )

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

    if submitted:

        actors = [
            actor.strip()
            for actor in actors_input.split(",")
        ]

        interaction_data = {
            "interaction_id":
                f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}",

            "timestamp":
                datetime.now().strftime("%Y-%m-%d"),

            "interaction_type":
                interaction_type,

            "actors":
                actors,

            "narrative":
                narrative,

            "pulse_impact": {
                "trust_pulse": trust_pulse,
                "participation_pulse": participation_pulse,
                "innovation_pulse": innovation_pulse
            }
        }

        filename = (
            f"interaction-"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )

        save_path = os.path.join(DATASET_DIR, filename)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(interaction_data, f, indent=4)

        st.success("Interaction saved successfully!")

        st.rerun()

# =========================================================
# MIDDLE PANEL — DASHBOARD
# =========================================================

with middle_col:
    if st.button("🗑 Reset Institutional Data"):

        for filename in os.listdir(DATASET_DIR):

            file_path = os.path.join(DATASET_DIR, filename)

            if os.path.isfile(file_path):

                os.remove(file_path)

        st.warning("All institutional interaction data has been reset.")

        st.rerun()
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

    st.subheader("AI Institutional Interpretation")

    if pulse_totals["trust_pulse"] <= -5:
        st.error(
            "Trust institutional climate is deteriorating."
        )

    if pulse_totals["participation_pulse"] <= -5:
        st.warning(
            "Participation deficit detected."
        )

    if pulse_totals["innovation_pulse"] <= -5:
        st.warning(
            "Innovation stagnation detected."
        )

    if (
        pulse_totals["trust_pulse"] >= 0
        and pulse_totals["participation_pulse"] >= 0
    ):
        st.success(
            "Institutional governance remains stable."
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

    st.metric(
        "Institutional Health",
        f"{health_score}/100"
    )

    st.divider()

    st.subheader("Institutional Risk Level")

    if health_score >= 85:
        st.success(
            "LOW RISK — Institutional governance is healthy."
        )

    elif health_score >= 70:
        st.warning(
            "MODERATE RISK — Governance tensions detected."
        )

    else:
        st.error(
            "HIGH RISK — Institutional instability escalating."
        )

# =========================================================
# RIGHT PANEL — ANALYTICS
# =========================================================

with right_col:

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

        progress_value = max(
            0.0,
            min(1.0, (value + 10) / 20)
        )

        st.progress(progress_value)

        st.write(f"Status: {color} ({value})")

    pulse_df = pd.DataFrame({
        "Pulse": list(pulse_totals.keys()),
        "Score": list(pulse_totals.values())
    })

    st.bar_chart(
        pulse_df.set_index("Pulse")
    )

# =========================================================
# FULL WIDTH ANALYTICS
# =========================================================

st.divider()

st.subheader("Institutional Pulse Timeline")

timeline_df = pd.DataFrame(timeline_data)

if not timeline_df.empty:

    timeline_df = timeline_df.sort_values("timestamp")

    st.line_chart(
        timeline_df.set_index("timestamp")[
            [
                "trust_pulse",
                "participation_pulse",
                "innovation_pulse"
            ]
        ]
    )

st.divider()

st.subheader("Institutional Actor Activity")

if actor_frequency:

    actor_df = pd.DataFrame({
        "Actor": list(actor_frequency.keys()),
        "Frequency": list(actor_frequency.values())
    })

    actor_df = actor_df.sort_values(
        by="Frequency",
        ascending=True
    )

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

if (
    pulse_totals["trust_pulse"] > -10
    and pulse_totals["participation_pulse"] > -10
    and pulse_totals["innovation_pulse"] > -10
):
    st.success(
        "✅ No major institutional governance threats detected."
    )

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

st.divider()

st.subheader("AI Governance Recommendation Engine")

recommendations = []

if pulse_totals["trust_pulse"] < -5:
    recommendations.append(
        "Increase institutional trust-building dialogue."
    )

if pulse_totals["participation_pulse"] < -5:
    recommendations.append(
        "Expand participatory governance mechanisms."
    )

if pulse_totals["innovation_pulse"] < -5:
    recommendations.append(
        "Encourage adaptive governance innovation labs."
    )

if len(actor_frequency) > 20:
    recommendations.append(
        "Governance network becoming fragmented."
    )

if recommendations:

    for rec in recommendations:
        st.warning(rec)

else:
    st.success(
        "Institutional governance conditions appear stable."
    )

st.divider()

st.subheader("What MakesCampus Governance Intelligence Different?")

st.markdown("""

### 🧠 General AI vs Institutional Governance AI

| General AI | Campus Governance Intelligence |
|---|---|
| General-purpose AI | Governance intelligence |
| Generic responses | Institutional diagnostics |
| No institutional memory | Governance memory |
| No pulse engine | Pulse analytics |
| No actor mapping | Network governance analysis |
| No early warning system | Governance risk engine |

### 🏛️ Campus Governance Intelligence Focus

- Institutional Governance Intelligence
- Organizational Pulse Monitoring
- AI-Assisted Governance Analytics
- Governance Risk Diagnostics
- Institutional Trust Monitoring
- Participation Dynamics Analysis

""")
