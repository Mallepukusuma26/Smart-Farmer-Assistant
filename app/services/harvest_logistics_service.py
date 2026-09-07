"""
Harvest Logistics Service Module for Smart Farmer Assistant.

Models combine harvester field capacity (acres/hr), grain transport bin requirements, and post-harvest loss reduction.
"""

from typing import Dict, Any, List


class HarvestLogisticsService:
    """Calculates combine harvester field capacity, grain transport truck trips, and harvest labor scheduling."""

    def calculate_harvest_capacity_and_trips(
        self,
        crop_name: str,
        total_acres: float,
        expected_yield_tons_per_acre: float,
        combine_cutter_bar_width_meters: float = 4.5,
        operating_speed_km_h: float = 5.0,
        truck_capacity_tons: float = 10.0
    ) -> Dict[str, Any]:
        """
        Theoretical Field Capacity (ha/hr) = (Width (m) * Speed (km/h)) / 10
        Effective Field Capacity (acres/hr) = Theoretical * Field Efficiency (0.70) * 2.47105
        """
        theoretical_ha_hr = (combine_cutter_bar_width_meters * operating_speed_km_h) / 10.0
        effective_acres_hr = round(theoretical_ha_hr * 0.70 * 2.47105, 2)

        total_harvest_hours = round(total_acres / max(0.1, effective_acres_hr), 1)
        total_yield_tons = round(total_acres * expected_yield_tons_per_acre, 2)

        truck_trips_needed = int((total_yield_tons / truck_capacity_tons) + 0.99) if truck_capacity_tons > 0 else 1

        return {
            "crop_name": crop_name,
            "total_acres": total_acres,
            "combine_working_width_m": combine_cutter_bar_width_meters,
            "operating_speed_km_h": operating_speed_km_h,
            "effective_field_capacity_acres_hr": effective_acres_hr,
            "total_harvest_duration_hours": total_harvest_hours,
            "estimated_total_yield_tons": total_yield_tons,
            "truck_capacity_tons": truck_capacity_tons,
            "total_transport_trips_required": truck_trips_needed,
            "harvest_efficiency_advice": f"Schedule {truck_trips_needed} truck dispatches to keep combine harvester operating without bin overflow downtime."
        }
