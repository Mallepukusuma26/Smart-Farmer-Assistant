"""
Agronomy Grain Storage Mycotoxin Risk Model for Smart Farmer Assistant.

Models Aspergillus flavus growth, Aflatoxin B1 accumulation risk (ppb), and storage aeration safety.
"""

from typing import Dict, Any


class AgronomyGrainMycotoxinRiskEngine:
    """Calculates Aflatoxin / Fusarium mycotoxin accumulation risk based on grain moisture % and temperature."""

    @staticmethod
    def calculate_mycotoxin_risk(
        grain_moisture_pct: float,
        storage_temp_c: float,
        storage_days: int = 30
    ) -> Dict[str, Any]:
        """
        Aspergillus growth occurs rapidly above 15% moisture and 25°C - 35°C.
        """
        moisture_risk = max(0.0, grain_moisture_pct - 13.5)
        temp_risk = max(0.0, storage_temp_c - 20.0)

        risk_score = round(min(100.0, (moisture_risk * 18.0) + (temp_risk * 2.5) + (storage_days * 0.5)), 1)

        risk_level = "HIGH AFLATOXIN RISK — IMMINENT SPOILAGE" if risk_score >= 65.0 else (
            "Moderate Mycotoxin Risk" if risk_score >= 30.0 else "Low Mycotoxin Risk (Safe Storage)"
        )

        return {
            "grain_moisture_pct": grain_moisture_pct,
            "storage_temp_c": storage_temp_c,
            "storage_days": storage_days,
            "mycotoxin_risk_score_100": risk_score,
            "risk_classification": risk_level,
            "safety_action": "Run high-capacity aeration fans immediately and dry grain below 13.0% moisture to halt fungal growth." if risk_score >= 40.0 else "Storage environmental conditions are stable."
        }
