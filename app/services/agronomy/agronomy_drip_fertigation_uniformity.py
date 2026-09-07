"""
Agronomy Drip Fertigation Uniformity Engine for Smart Farmer Assistant.

Evaluates drip fertigation concentration uniformity, Christiansen's Uniformity (CU), and emission point variance.
"""

from typing import Dict, Any, List


class AgronomyDripFertigationUniformityEngine:
    """Calculates fertigation emission concentration uniformity across drip laterals."""

    @staticmethod
    def calculate_fertigation_uniformity(emitter_concentrations_ppm: List[float]) -> Dict[str, Any]:
        """Calculates Christiansen's Uniformity Coefficient (CU %) for liquid fertilizer injection."""
        if not emitter_concentrations_ppm:
            return {"error": "Emitter concentration list cannot be empty."}

        mean_conc = float(sum(emitter_concentrations_ppm) / len(emitter_concentrations_ppm))
        if mean_conc <= 0:
            return {"error": "Mean concentration must be greater than zero."}

        abs_deviations = [abs(x - mean_conc) for x in emitter_concentrations_ppm]
        mean_deviation = sum(abs_deviations) / len(abs_deviations)

        cu_pct = round((1.0 - (mean_deviation / mean_conc)) * 100.0, 2)
        cu_pct = max(0.0, min(100.0, cu_pct))

        rating = "Excellent Uniformity" if cu_pct >= 90.0 else ("Acceptable Uniformity" if cu_pct >= 80.0 else "Poor Uniformity — Check Venturi Injector")

        return {
            "mean_fertilizer_concentration_ppm": round(mean_conc, 1),
            "sample_points_count": len(emitter_concentrations_ppm),
            "christiansen_uniformity_pct": cu_pct,
            "fertigation_quality_rating": rating,
            "min_concentration_ppm": min(emitter_concentrations_ppm),
            "max_concentration_ppm": max(emitter_concentrations_ppm)
        }
