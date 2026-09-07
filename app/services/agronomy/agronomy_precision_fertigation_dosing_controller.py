"""
Agronomy Precision Fertigation Dosing Controller Engine for Smart Farmer Assistant.

Models automated Venturi liquid fertilizer injection, target EC (dS/m), target pH, and stock solution blending ratio.
"""

from typing import Dict, Any, List


class AgronomyPrecisionFertigationDosingEngine:
    """Calculates stock solution A/B tank injection rates (L/hr) for hydroponic and drip fertigation systems."""

    @staticmethod
    def calculate_dosing_rates(
        target_ec_ds_m: float,
        target_ph: float,
        water_flow_rate_lph: float,
        raw_water_ec_ds_m: float = 0.3,
        stock_solution_concentration_factor: float = 100.0
    ) -> Dict[str, Any]:
        """
        Target EC Boost = Target EC - Raw Water EC
        Injection Rate (L/hr) = (Flow Rate * EC Boost) / (Stock Concentration * 1.2)
        """
        ec_boost_needed = max(0.1, target_ec_ds_m - raw_water_ec_ds_m)

        # Stock A and Stock B injection rates in L/hr
        tank_a_injection_lph = round((water_flow_rate_lph * ec_boost_needed * 0.5) / (stock_solution_concentration_factor * 1.1), 2)
        tank_b_injection_lph = round((water_flow_rate_lph * ec_boost_needed * 0.5) / (stock_solution_concentration_factor * 1.1), 2)

        # Acid injection rate for pH control (Nitric / Phosphoric Acid 10% sol)
        acid_injection_ml_hr = round(water_flow_rate_lph * max(0.0, target_ph - 5.8) * 15.0, 1)

        return {
            "target_ec_ds_m": target_ec_ds_m,
            "target_ph": target_ph,
            "raw_water_ec_ds_m": raw_water_ec_ds_m,
            "water_flow_rate_lph": water_flow_rate_lph,
            "stock_tank_a_injection_rate_lph": tank_a_injection_lph,
            "stock_tank_b_injection_rate_lph": tank_b_injection_lph,
            "acid_injection_rate_ml_hr": acid_injection_ml_hr,
            "fertigation_control_status": f"Maintain Tank A: {tank_a_injection_lph} L/hr, Tank B: {tank_b_injection_lph} L/hr to achieve EC {target_ec_ds_m} dS/m."
        }
