"""
Agronomy Crop Rotation Benefit Analyzer Engine for Smart Farmer Assistant.

Quantifies yield advantage and pest break benefits of legume-cereal crop rotations.
"""
from typing import Dict, Any

class AgronomyCropRotationBenefitAnalyzerEngine:
    @staticmethod
    def analyze_rotation_benefit(previous_crop: str, current_crop: str) -> Dict[str, Any]:
        n_credit_kg_ha = 0.0
        yield_boost_pct = 0.0
        disease_break_score = 'Standard'

        prev = previous_crop.lower()
        curr = current_crop.lower()

        if any(legume in prev for legume in ['chickpea', 'pigeonpea', 'soybean', 'groundnut', 'lentil', 'cowpea']):
            n_credit_kg_ha = 30.0
            yield_boost_pct = 12.5
            disease_break_score = 'Excellent Disease/Pest Break'
        elif prev != curr:
            yield_boost_pct = 5.0
            disease_break_score = 'Moderate Break'

        return {
            'previous_crop': previous_crop,
            'current_crop': current_crop,
            'nitrogen_credit_kg_ha': n_credit_kg_ha,
            'expected_yield_boost_pct': yield_boost_pct,
            'disease_break_evaluation': disease_break_score
        }
