"""
Agronomy Irrigation Surge Flow Furrow Engine for Smart Farmer Assistant.

Models surge flow furrow irrigation cycles, advance phase reduction, and deep percolation water savings.
"""

from typing import Dict, Any


class AgronomyIrrigationSurgeFlowEngine:
    """Calculates surge flow cycle times (on/off minutes) and furrow advance efficiency."""

    @staticmethod
    def calculate_surge_flow_cycles(
        furrow_length_m: float,
        flow_rate_lps: float = 2.5,
        soil_intake_family: str = "Medium Loam"
    ) -> Dict[str, Any]:
        """Calculates 4-cycle surge advance timing to reduce tailwater runoff and percolation losses."""
        t_advance = max(30.0, furrow_length_m * 0.45)  # minutes for 100% advance under continuous flow

        # 4 Surge Cycles (On/Off split)
        c1 = round(t_advance * 0.15, 1)
        c2 = round(t_advance * 0.25, 1)
        c3 = round(t_advance * 0.35, 1)
        c4 = round(t_advance * 0.25, 1)

        water_savings_pct = 25.0

        return {
            "furrow_length_m": furrow_length_m,
            "inflow_rate_lps": flow_rate_lps,
            "estimated_continuous_advance_minutes": round(t_advance, 1),
            "surge_cycle_schedule_minutes": [
                {"cycle": 1, "on_time_min": c1, "off_time_min": c1},
                {"cycle": 2, "on_time_min": c2, "off_time_min": c2},
                {"cycle": 3, "on_time_min": c3, "off_time_min": c3},
                {"cycle": 4, "on_time_min": c4, "off_time_min": c4}
            ],
            "estimated_water_savings_pct": water_savings_pct,
            "surge_irrigation_benefit": "Intermittent wetting consolidates furrow surface soil pores, accelerating water advance to the lower end."
        }
