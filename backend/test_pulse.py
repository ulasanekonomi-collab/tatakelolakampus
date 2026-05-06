from pulse_engine import InstitutionalPulseEngine

sample_interactions = [

    {
        "pulse_impact": {
            "trust_pulse": -2,
            "participation_pulse": -1,
            "innovation_pulse": 1
        },

        "organizational_signals": [
            "coordination_overlap",
            "fatigue"
        ]
    },

    {
        "pulse_impact": {
            "trust_pulse": 3,
            "participation_pulse": 2,
            "innovation_pulse": 2
        },

        "organizational_signals": [
            "cross_unit_collaboration"
        ]
    }
]

engine = InstitutionalPulseEngine()

result = engine.calculate_pulse(sample_interactions)

print(result)
