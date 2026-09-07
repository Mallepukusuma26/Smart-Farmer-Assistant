"""
Agronomy Drip Filter Backwash Schedule Engine for Smart Farmer Assistant.

Models media filter pressure differential (Delta-P), backwash frequency, and flush cycle duration.
"""

from typing import Dict, Any


class AgronomyDripFilterBackwashEngine:
    """Calculates drip irrigation media filter flushing intervals based on water turbidity (NTU) and pressure drop."""

    @staticmethod
    def calculate_backwash_schedule(
        water_turbidity_ntu: float,
        filter_flow_m3_hr: float,
        initial_pressure_bar: float = 3.5,
        current_pressure_bar: float = 4.1
    ) -> Dict[str, Any]:
        """Backwash flush triggered when Delta-P exceeds 0.5 bar (50 kPa)."""
        delta_p_bar = round(current_pressure_bar - initial_pressure_bar, 2)
        needs_backwash = delta_p_bar >= 0.5

        # Interval estimation based on turbidity
        if water_turbidity_ntu > 50:
            flush_interval_hours = 2.0
        elif water_turbidity_ntu > 20:
            flush_interval_hours = 4.0
        elif water_turbidity_ntu > 5:
            flush_interval_hours = 8.0
        else:
            flush_interval_hours = 24.0

        flush_water_m3 = round((filter_flow_m3_hr * 0.15) * (90.0 / 3600.0), 2)  # 90 second flush cycle

        return {
            "water_turbidity_ntu": water_turbidity_ntu,
            "pressure_differential_bar": delta_p_bar,
            "backwash_urgency": "IMMEDIATE BACKWASH REQUIRED" if needs_backwash else "Normal Filter Operation",
            "recommended_flush_interval_hours": flush_interval_hours,
            "flush_cycle_duration_seconds": 90,
            "estimated_water_used_per_flush_m3": flush_water_m3,
            "maintenance_tip": "Inspect disc/screen elements for organic algae slime if backwash frequency drops below 2 hours."
        }
