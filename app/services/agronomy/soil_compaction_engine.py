"""
Soil Compaction & Bulk Density Dynamics Engine.
Calculates penetrometer resistance, total porosity, root elongation restriction,
and subsoiling tillage depth requirements.
"""

import math
from typing import Dict, Any

class SoilCompactionEngine:
    """Soil penetrometer resistance and bulk density calculator."""

    def calculate_bulk_density_porosity(
        self, dry_soil_mass_g: float, core_volume_cm3: float, particle_density_g_cm3: float = 2.65
    ) -> Dict[str, float]:
        """
        Calculate dry bulk density (rho_b = M_s / V_t) and total porosity (f = 1 - rho_b / rho_p).
        """
        bulk_density = dry_soil_mass_g / max(0.1, core_volume_cm3)
        porosity_pct = (1.0 - (bulk_density / particle_density_g_cm3)) * 100.0

        # Critical bulk density thresholds for root penetration restriction
        critical_threshold = 1.65  # g/cm3 for loam/clay loam
        root_restriction = bulk_density >= critical_threshold

        return {
            "dry_bulk_density_g_cm3": round(bulk_density, 2),
            "particle_density_g_cm3": particle_density_g_cm3,
            "total_porosity_pct": round(porosity_pct, 1),
            "critical_threshold_g_cm3": critical_threshold,
            "root_growth_restricted": root_restriction,
            "compaction_rating": "Severe" if bulk_density > 1.70 else ("Moderate" if bulk_density > 1.50 else "Optimal")
        }

    def calculate_penetrometer_resistance(
        self, depth_cm: float, cone_index_kpa: float, moisture_vwc: float
    ) -> Dict[str, Any]:
        """
        Evaluate cone index penetrometer resistance vs soil moisture.
        Root growth is severely inhibited above 2,000 kPa (2.0 MPa).
        """
        adjusted_cone_index = cone_index_kpa * (0.35 / max(0.1, moisture_vwc))
        subsoiling_needed = adjusted_cone_index > 2000.0

        return {
            "depth_cm": depth_cm,
            "raw_cone_index_kpa": cone_index_kpa,
            "moisture_corrected_cone_index_kpa": round(adjusted_cone_index, 1),
            "penetration_resistance_mpa": round(adjusted_cone_index / 1000.0, 2),
            "subsoiling_tillage_recommended": subsoiling_needed,
            "recommended_tillage_depth_cm": round(depth_cm + 10.0, 0) if subsoiling_needed else 0.0
        }
