"""
Soil Nutrient Dynamics & Mineralization Kinetics Engine.
Calculates organic Nitrogen mineralization, Phosphorus sorption dynamics,
and Potassium cation exchange kinetics.
"""

import math
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class SoilNutrientProfile:
    organic_matter_pct: float
    clay_pct: float
    sand_pct: float
    ph: float
    cation_exchange_capacity_meq_100g: float
    soil_temp_c: float
    volumetric_water_content: float

class SoilNutrientDynamicsEngine:
    """Soil chemical kinetics and nutrient bio-availability dynamics."""

    def __init__(self):
        pass

    def calculate_n_mineralization(self, organic_matter_pct: float, soil_temp_c: float, moisture_vwc: float) -> float:
        """
        Estimate annual Nitrogen mineralization (kg N/ha/yr).
        Uses first-order kinetics with Arrhenius temperature adjustment and moisture factor.
        """
        # Base pool (approx 2% N in OM, 1-3% mineralized annually)
        total_n_kg_ha = organic_matter_pct * 0.05 * 2000000 * 0.001  # Top 15cm soil mass ~2M kg/ha
        k_base = 0.015  # Base rate per year
        
        # Temperature factor Q10 = 2.0 (reference at 25C)
        temp_factor = 2.0 ** ((soil_temp_c - 25.0) / 10.0)
        temp_factor = max(0.1, min(2.5, temp_factor))

        # Moisture factor (optimal between field capacity 0.25 - 0.35 VWC)
        if moisture_vwc < 0.1:
            moisture_factor = 0.2
        elif moisture_vwc < 0.3:
            moisture_factor = moisture_vwc / 0.3
        elif moisture_vwc <= 0.4:
            moisture_factor = 1.0
        else:
            moisture_factor = max(0.3, 1.0 - (moisture_vwc - 0.4) * 2.0)

        n_mineralized_kg_ha = total_n_kg_ha * k_base * temp_factor * moisture_factor
        return round(n_mineralized_kg_ha, 2)

    def calculate_p_sorption_isotherm(self, ph: float, clay_pct: float, olsen_p_ppm: float) -> Dict[str, float]:
        """
        Calculate Phosphorus fixation capacity and bio-available P fraction using Langmuir sorption kinetics.
        """
        # P fixation is highest at low pH (<5.5, Al/Fe binding) and high pH (>7.5, Ca binding)
        if ph < 5.5:
            fixation_index = 0.85 - (ph - 4.0) * 0.1
        elif ph > 7.5:
            fixation_index = 0.50 + (ph - 7.5) * 0.15
        else:
            fixation_index = 0.20 + abs(ph - 6.5) * 0.1

        fixation_index = max(0.15, min(0.95, fixation_index + (clay_pct / 100.0) * 0.2))

        # Langmuir maximum adsorption capacity (mg P / kg soil)
        q_max = 200.0 + clay_pct * 8.0 + (7.0 - ph) * 20.0
        q_max = max(100.0, q_max)

        available_p_kg_ha = olsen_p_ppm * 2.24 * (1.0 - fixation_index * 0.5)

        return {
            "p_fixation_index": round(fixation_index, 3),
            "max_adsorption_capacity_mg_kg": round(q_max, 1),
            "effective_available_p_kg_ha": round(available_p_kg_ha, 2),
            "optimal_ph_range": "6.0 - 7.2"
        }

    def calculate_k_exchange_dynamics(self, cec: float, exchangeable_k_ppm: float, clay_pct: float) -> Dict[str, float]:
        """
        Calculate Potassium CEC saturation percentage and non-exchangeable K buffering capacity.
        """
        # Exchangeable K in meq/100g = K_ppm / 391.0
        k_meq = exchangeable_k_ppm / 391.0
        k_saturation_pct = (k_meq / max(1.0, cec)) * 100.0

        # Optimal K saturation is 3% - 5% of CEC
        if k_saturation_pct < 2.0:
            status = "Deficient"
        elif k_saturation_pct <= 5.0:
            status = "Optimum"
        else:
            status = "Excessive"

        non_exchangeable_buffer_kg_ha = exchangeable_k_ppm * 2.24 * (1.0 + (clay_pct / 50.0))

        return {
            "k_saturation_pct": round(k_saturation_pct, 2),
            "k_status": status,
            "buffering_capacity_kg_ha": round(non_exchangeable_buffer_kg_ha, 2)
        }
