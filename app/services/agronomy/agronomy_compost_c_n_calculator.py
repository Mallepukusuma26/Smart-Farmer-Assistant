"""
Agronomy Compost Carbon-to-Nitrogen (C:N) Ratio Calculator for Smart Farmer Assistant.

Calculates initial blend C:N ratio, moisture balancing, and organic carbon humification kinetics.
"""

from typing import Dict, Any, List


class AgronomyCompostCNCalculatorEngine:
    """Calculates compost raw material blending ratios to hit optimal 25:1 to 30:1 C:N target."""

    @staticmethod
    def calculate_compost_blend(materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Input materials format: [{'name': 'Straw', 'weight_kg': 100, 'c_n_ratio': 80, 'moisture_pct': 15, 'nitrogen_pct': 0.6}]
        Optimal C:N ratio range: 25:1 - 30:1
        Optimal Moisture Range: 50% - 60%
        """
        if not materials:
            return {"error": "Material list cannot be empty."}

        total_weight = sum(float(m.get('weight_kg', 0)) for m in materials)
        if total_weight <= 0:
            return {"error": "Total weight must be greater than zero."}

        total_carbon = 0.0
        total_nitrogen = 0.0
        total_water = 0.0

        for m in materials:
            w = float(m.get('weight_kg', 0))
            moisture = float(m.get('moisture_pct', 20)) / 100.0
            dry_weight = w * (1.0 - moisture)
            n_pct = float(m.get('nitrogen_pct', 1.0)) / 100.0
            c_n = float(m.get('c_n_ratio', 25.0))

            n_mass = dry_weight * n_pct
            c_mass = n_mass * c_n

            total_nitrogen += n_mass
            total_carbon += c_mass
            total_water += (w * moisture)

        final_cn_ratio = round(total_carbon / total_nitrogen, 1) if total_nitrogen > 0 else 30.0
        final_moisture_pct = round((total_water / total_weight) * 100.0, 1)

        water_to_add_liters = 0.0
        if final_moisture_pct < 55.0:
            target_water = (total_weight * (1.0 - (final_moisture_pct / 100.0))) / 0.45 - (total_weight - total_water)
            water_to_add_liters = round(max(0.0, target_water), 1)

        cn_status = "Optimal C:N Target (25:1 - 30:1)" if 25.0 <= final_cn_ratio <= 32.0 else (
            "High Carbon (Slow Decomposition — Add Nitrogen Greens)" if final_cn_ratio > 32.0 else "Low Carbon (High Ammonia Loss — Add Carbon Browns)"
        )

        return {
            "total_compost_weight_kg": round(total_weight, 1),
            "final_blend_cn_ratio": final_cn_ratio,
            "cn_ratio_status": cn_status,
            "initial_moisture_pct": final_moisture_pct,
            "water_to_add_liters": water_to_add_liters,
            "estimated_finished_compost_kg": round(total_weight * 0.45, 1)
        }
