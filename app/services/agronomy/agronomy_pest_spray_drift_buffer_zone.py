"""
Agronomy Pest Spray Drift Buffer Zone Engine for Smart Farmer Assistant.

Models pesticide droplet drift distance (meters), wind speed impact, boom height, and mandatory buffer zone width.
"""

import math
from typing import Dict, Any


class AgronomyPestSprayDriftBufferEngine:
    """Calculates downwind buffer zone distance (meters) based on nozzle droplet VMD (µm) and wind speed (m/s)."""

    @staticmethod
    def calculate_spray_buffer_zone(
        wind_speed_m_s: float,
        boom_height_m: float = 0.75,
        droplet_vmd_microns: float = 250.0,
        sensitive_boundary_distance_m: float = 30.0
    ) -> Dict[str, Any]:
        """
        Drift Distance = (Wind Speed * Boom Height * 250) / Droplet VMD
        """
        drift_distance_m = round((wind_speed_m_s * boom_height_m * 250.0) / max(100.0, droplet_vmd_microns), 1)

        safe_distance_m = round(max(5.0, drift_distance_m * 1.5), 1)
        spray_allowed = wind_speed_m_s <= 5.0 and safe_distance_m <= sensitive_boundary_distance_m

        drift_risk = "HIGH DRIFT RISK — DO NOT SPRAY" if wind_speed_m_s > 5.0 else (
            "Moderate Drift Risk (Use Air-Induction Nozzles)" if drift_distance_m > 10.0 else "Low Spray Drift Risk"
        )

        return {
            "wind_speed_m_s": wind_speed_m_s,
            "boom_height_m": boom_height_m,
            "droplet_vmd_microns": droplet_vmd_microns,
            "calculated_drift_distance_m": drift_distance_m,
            "recommended_buffer_zone_m": safe_distance_m,
            "spray_permitted": spray_allowed,
            "drift_risk_category": drift_risk,
            "nozzle_recommendation": "Switch to Air-Induction Coarse (AIC) nozzles to generate > 350 µm droplets under breezy conditions." if drift_distance_m > 10.0 else "Standard medium droplet nozzles acceptable."
        }
