"""
Agronomy Subsurface Tile Drainage Design Engine for Smart Farmer Assistant.

Models Hooghoudt's water table drawdown equation, lateral drain pipe spacing (m), and drainage discharge coefficient.
"""

import math
from typing import Dict, Any


class AgronomySubsurfaceTileDrainageDesignEngine:
    """Calculates subsurface agricultural tile drainage lateral pipe spacing using Hooghoudt's equation."""

    @staticmethod
    def calculate_tile_drain_spacing(
        soil_hydraulic_conductivity_m_day: float,
        drainage_coefficient_mm_day: float = 12.0,
        impermeable_layer_depth_m: float = 3.0,
        target_water_table_depth_m: float = 1.0,
        drain_pipe_depth_m: float = 1.5,
        pipe_radius_m: float = 0.05
    ) -> Dict[str, Any]:
        """
        Hooghoudt's Equation: S^2 = (8 * K * d * h + 4 * K * h^2) / q
        S = Drain spacing (m)
        K = Hydraulic conductivity (m/day)
        h = Hydraulic head mid-way between drains (m)
        q = Drainage discharge rate (m/day)
        """
        q = max(0.001, drainage_coefficient_mm_day / 1000.0)
        h = max(0.1, drain_pipe_depth_m - target_water_table_depth_m)
        d = max(0.2, impermeable_layer_depth_m - drain_pipe_depth_m)

        # Hooghoudt's simplified formulation
        s_squared = ((8.0 * soil_hydraulic_conductivity_m_day * d * h) + (4.0 * soil_hydraulic_conductivity_m_day * (h ** 2))) / q
        spacing_m = round(math.sqrt(max(1.0, s_squared)), 1)
        spacing_m = max(5.0, min(60.0, spacing_m))

        pipes_per_ha = round(10000.0 / spacing_m, 1)

        return {
            "hydraulic_conductivity_m_day": soil_hydraulic_conductivity_m_day,
            "drainage_coefficient_mm_day": drainage_coefficient_mm_day,
            "impermeable_layer_depth_m": impermeable_layer_depth_m,
            "drain_depth_m": drain_pipe_depth_m,
            "recommended_lateral_spacing_m": spacing_m,
            "required_tile_length_m_per_ha": pipes_per_ha,
            "water_table_management_goal": f"Maintains water table at {target_water_table_depth_m}m depth to prevent root zone waterlogging."
        }
