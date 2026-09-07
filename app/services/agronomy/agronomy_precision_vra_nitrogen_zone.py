"""
Agronomy Precision VRA Nitrogen Zone Engine for Smart Farmer Assistant.

Models Variable Rate Application (VRA) fertilizer map generation based on NDVI grid zones and soil SOM clusters.
"""

from typing import Dict, Any, List


class AgronomyPrecisionVRANitrogenEngine:
    """Calculates variable rate nitrogen prescription maps (kg/ha) across high/medium/low vigor zone clusters."""

    @staticmethod
    def calculate_vra_nitrogen_prescription(
        field_area_ha: float,
        ndvi_grid_values: List[float],
        flat_rate_n_kg_ha: float = 120.0
    ) -> Dict[str, Any]:
        """
        VRA Prescription Rule:
        - Low NDVI Zone (Stress): Apply Flat + 20%
        - Medium NDVI Zone (Target): Apply Flat Rate
        - High NDVI Zone (Vigorous): Apply Flat - 15% (avoid lodging/waste)
        """
        if not ndvi_grid_values:
            return {"error": "NDVI grid values list cannot be empty."}

        avg_ndvi = sum(ndvi_grid_values) / len(ndvi_grid_values)

        zones = []
        total_vra_n_kg = 0.0

        for idx, ndvi in enumerate(ndvi_grid_values):
            if ndvi < 0.4:
                zone_type = "Low Vigor Zone"
                n_rate = round(flat_rate_n_kg_ha * 1.20, 1)
            elif ndvi < 0.7:
                zone_type = "Medium Vigor Zone"
                n_rate = round(flat_rate_n_kg_ha * 1.00, 1)
            else:
                zone_type = "High Vigor Zone"
                n_rate = round(flat_rate_n_kg_ha * 0.85, 1)

            zone_area = round(field_area_ha / len(ndvi_grid_values), 2)
            total_vra_n_kg += (n_rate * zone_area)

            zones.append({
                "cell_id": idx + 1,
                "ndvi_value": round(ndvi, 3),
                "zone_type": zone_type,
                "prescribed_n_rate_kg_ha": n_rate,
                "cell_area_ha": zone_area
            })

        flat_total_n_kg = round(flat_rate_n_kg_ha * field_area_ha, 1)
        savings_kg = round(flat_total_n_kg - total_vra_n_kg, 1)

        return {
            "field_area_ha": field_area_ha,
            "average_field_ndvi": round(avg_ndvi, 3),
            "flat_rate_total_nitrogen_kg": flat_total_n_kg,
            "vra_prescription_total_nitrogen_kg": round(total_vra_n_kg, 1),
            "net_nitrogen_saved_kg": savings_kg,
            "nitrogen_cost_saved_inr": round(savings_kg * 13.0, 2),  # Urea cost proxy
            "prescription_grid_zones": zones
        }
