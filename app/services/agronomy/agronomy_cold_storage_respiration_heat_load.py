"""
Agronomy Cold Storage Respiration & Heat Load Engine for Smart Farmer Assistant.

Models post-harvest fruit/vegetable respiration heat generation (W/ton), ethylene production, and refrigeration tonnage.
"""

from typing import Dict, Any


class AgronomyColdStorageRespirationEngine:
    """Calculates crop respiration heat generation and cold room refrigeration capacity (Tons of Refrigeration - TR)."""

    @staticmethod
    def calculate_respiration_heat_load(
        crop_type: str,
        storage_temp_c: float,
        crop_tonnage: float = 50.0,
        room_volume_m3: float = 300.0
    ) -> Dict[str, Any]:
        """
        Respiration Heat (mW/kg) = A * (T^B)
        1 TR = 3.517 kW = 3517 Watts
        """
        # Respiration intensity factors (mW/kg at storage temp)
        crop_factors = {
            "Apple": 12.5,
            "Potato": 18.0,
            "Tomato": 35.0,
            "Banana": 45.0,
            "Strawberry": 65.0,
            "Spinach": 110.0
        }

        resp_factor = crop_factors.get(crop_type, 25.0)
        # Heat generation per ton = factor * 1000 kg / 1000 = W/ton
        heat_gen_watts_per_ton = resp_factor * (1.0 + (storage_temp_c * 0.08))
        total_respiration_heat_kw = (heat_gen_watts_per_ton * crop_tonnage) / 1000.0

        # Transmission + infiltration load (~1.5x respiration)
        total_cooling_load_kw = total_respiration_heat_kw * 2.5
        required_refrigeration_tr = round(max(1.5, total_cooling_load_kw / 3.517), 2)

        return {
            "crop_type": crop_type,
            "storage_temperature_c": storage_temp_c,
            "stored_crop_tonnage": crop_tonnage,
            "respiration_heat_watts_per_ton": round(heat_gen_watts_per_ton, 1),
            "total_respiration_heat_kw": round(total_respiration_heat_kw, 2),
            "total_cooling_load_kw": round(total_cooling_load_kw, 2),
            "required_refrigeration_tr": required_refrigeration_tr,
            "storage_atmosphere_advice": f"Maintain relative humidity at 90-95% and ethylene scrubbing to prevent premature ripening of stored {crop_type}."
        }
