from typing import Dict, List


class InstitutionalPulseEngine:

    def __init__(self):

        self.default_state = {
            "trust_pulse": 0,
            "participation_pulse": 0,
            "innovation_pulse": 0,
            "fatigue_pulse": 0,
            "coordination_pulse": 0
        }

    def calculate_pulse(self, interactions: List[Dict]) -> Dict:

        pulse = self.default_state.copy()

        for interaction in interactions:

            pulse_data = interaction.get("pulse_impact", {})

            pulse["trust_pulse"] += pulse_data.get("trust_pulse", 0)

            pulse["participation_pulse"] += pulse_data.get(
                "participation_pulse",
                0
            )

            pulse["innovation_pulse"] += pulse_data.get(
                "innovation_pulse",
                0
            )

            organizational_signals = interaction.get(
                "organizational_signals",
                []
            )

            if "fatigue" in organizational_signals:
                pulse["fatigue_pulse"] += 1

            if "coordination_overlap" in organizational_signals:
                pulse["coordination_pulse"] -= 1

            if "cross_unit_collaboration" in organizational_signals:
                pulse["coordination_pulse"] += 1

        return pulse
