"""
Irrigation Hydraulics & Pipe Friction Loss Engine.
Calculates Hazen-Williams pressure drop and emitter Christiansen Uniformity (CU).
"""

import math
from typing import Dict, Any

class IrrigationHydraulicsEngine:
    """Irrigation hydraulic pipe friction and emitter uniformity calculator."""

    def calculate_pipe_friction_loss(
        self, flow_rate_lps: float, pipe_diameter_mm: float, pipe_length_m: float, hazen_williams_c: float = 150.0
    ) -> Dict[str, float]:
        """
        Hazen-Williams Head Loss Equation:
        h_f = (10.67 * L * Q^1.852) / (C^1.852 * D^4.87)
        """
        Q_m3s = flow_rate_lps / 1000.0
        D_m = pipe_diameter_mm / 1000.0
        L_m = pipe_length_m
        C = hazen_williams_c

        head_loss_m = (10.67 * L_m * (Q_m3s ** 1.852)) / ((C ** 1.852) * (D_m ** 4.87))
        pressure_drop_kpa = head_loss_m * 9.81

        return {
            "flow_rate_lps": flow_rate_lps,
            "pipe_diameter_mm": pipe_diameter_mm,
            "pipe_length_m": pipe_length_m,
            "head_loss_meters": round(head_loss_m, 2),
            "pressure_drop_kpa": round(pressure_drop_kpa, 2)
        }
