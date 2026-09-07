"""
Agricultural Greenhouse Gas (GHG) & Soil Carbon Sequestration Engine.
Implements IPCC Tier 1 and Tier 2 methodology for N2O emissions,
methane flux, and Soil Organic Carbon (SOC) stock change calculations.
"""

from typing import Dict, Any

class GreenhouseGasCarbonEngine:
    """IPCC Tier 1/2 agricultural emission and carbon sequestration calculator."""

    def calculate_n2o_emissions(
        self, synthetic_n_kg: float, organic_n_kg: float, crop_residue_n_kg: float = 0.0
    ) -> Dict[str, float]:
        """
        Direct and indirect N2O emissions from soil inputs.
        IPCC Default EF1 = 0.01 (1% of N input converted to N2O-N).
        """
        total_n_input = synthetic_n_kg + organic_n_kg + crop_residue_n_kg
        
        # Direct N2O-N emissions (kg N2O-N)
        direct_n2o_n = total_n_input * 0.01

        # Indirect N2O from atmospheric deposition (FracGASM * EF4)
        volatilized_n = synthetic_n_kg * 0.10 + organic_n_kg * 0.20
        indirect_dep_n2o_n = volatilized_n * 0.01

        # Indirect N2O from leaching (FracLEACH * EF5)
        leached_n = total_n_input * 0.30
        indirect_leach_n2o_n = leached_n * 0.0075

        total_n2o_n = direct_n2o_n + indirect_dep_n2o_n + indirect_leach_n2o_n
        total_n2o_kg = total_n2o_n * (44.0 / 28.0)  # Molecular weight ratio N2O/N2
        co2_equivalent_kg = total_n2o_kg * 273.0  # GWP 100-yr factor for N2O = 273

        return {
            "total_nitrogen_applied_kg": round(total_n_input, 2),
            "direct_n2o_kg": round(direct_n2o_n * (44.0 / 28.0), 3),
            "indirect_n2o_kg": round((indirect_dep_n2o_n + indirect_leach_n2o_n) * (44.0 / 28.0), 3),
            "total_n2o_emissions_kg": round(total_n2o_kg, 3),
            "co2_equivalent_emissions_kg": round(co2_equivalent_kg, 2)
        }

    def calculate_soc_sequestration(
        self, base_soc_ton_ha: float, tillage_practice: str = "no_till", organic_amendment_ton_ha: float = 5.0
    ) -> Dict[str, float]:
        """
        Soil Organic Carbon (SOC) annual accumulation estimation.
        """
        tillage_factors = {
            "conventional": 1.0,
            "reduced": 1.08,
            "no_till": 1.15
        }
        f_mg = tillage_factors.get(tillage_practice.lower(), 1.0)
        
        # Organic amendment carbon transfer (approx 0.15 C fraction converted to persistent SOC)
        c_added = organic_amendment_ton_ha * 0.35 * 0.15

        annual_soc_gain = base_soc_ton_ha * (f_mg - 1.0) * 0.05 + c_added
        co2_sequestered_ton_ha = annual_soc_gain * (44.0 / 12.0)

        return {
            "initial_soc_ton_ha": base_soc_ton_ha,
            "annual_soc_gain_ton_ha": round(annual_soc_gain, 3),
            "net_co2_sequestered_ton_ha": round(co2_sequestered_ton_ha, 3),
            "projected_soc_5yr": round(base_soc_ton_ha + annual_soc_gain * 5.0, 2)
        }
