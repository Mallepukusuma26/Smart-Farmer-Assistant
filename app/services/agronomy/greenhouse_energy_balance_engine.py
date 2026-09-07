"""
Greenhouse Energy Balance & Thermal Heating Load Engine.
Calculates solar radiation gain, envelope conduction heat loss, ventilation heat loss,
and net thermal heating/cooling load in kW.
"""

from typing import Dict, Any

class GreenhouseEnergyBalanceEngine:
    """Greenhouse thermal modeling and HVAC sizing calculator."""

    def calculate_thermal_loads(
        self,
        surface_area_m2: float,
        glazing_u_value_w_m2_k: float,
        target_indoor_temp_c: float,
        outdoor_temp_c: float,
        ventilation_rate_m3_s: float,
        solar_irradiance_w_m2: float,
        glazing_transmissivity: float = 0.75
    ) -> Dict[str, float]:
        """
        Net Heat Load = Conduction Loss + Ventilation Loss - Solar Heat Gain
        """
        delta_t = target_indoor_temp_c - outdoor_temp_c
        
        # Conduction loss Q_cond = U * A * DeltaT
        q_conduction_w = glazing_u_value_w_m2_k * surface_area_m2 * delta_t

        # Ventilation loss Q_vent = V_dot * rho * Cp * DeltaT
        rho_air = 1.2  # kg/m3
        cp_air = 1005.0  # J/kg.K
        q_ventilation_w = ventilation_rate_m3_s * rho_air * cp_air * delta_t

        # Solar gain Q_solar = Irradiance * Area * Transmissivity
        q_solar_w = solar_irradiance_w_m2 * surface_area_m2 * glazing_transmissivity

        net_load_w = q_conduction_w + q_ventilation_w - q_solar_w
        net_load_kw = net_load_w / 1000.0

        return {
            "conduction_loss_kw": round(q_conduction_w / 1000.0, 2),
            "ventilation_loss_kw": round(q_ventilation_w / 1000.0, 2),
            "solar_heat_gain_kw": round(q_solar_w / 1000.0, 2),
            "net_heating_required_kw": round(max(0.0, net_load_kw), 2),
            "net_cooling_required_kw": round(max(0.0, -net_load_kw), 2)
        }
