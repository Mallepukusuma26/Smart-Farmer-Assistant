"""
Agronomy Soil Microbial Carbon Kinetics Engine for Smart Farmer Assistant.

Models microbial biomass carbon (MBC), metabolic quotient (qCO2), and soil respiration kinetics.
"""

from typing import Dict, Any


class AgronomySoilMicrobialKineticsEngine:
    """Calculates microbial biomass carbon (MBC in mg/kg) and metabolic quotient (qCO2 in ug CO2-C/mg MBC/hr)."""

    @staticmethod
    def calculate_microbial_kinetics(
        organic_carbon_pct: float,
        basal_respiration_mg_co2_kg_day: float,
        microbial_biomass_c_mg_kg: float = 250.0
    ) -> Dict[str, Any]:
        """
        qCO2 = (Basal Respiration / 24) / MBC
        MBC/SOC ratio = (MBC / (SOC_pct * 10000)) * 100
        """
        soc_mg_kg = organic_carbon_pct * 10000.0
        mbc_soc_ratio_pct = round((microbial_biomass_c_mg_kg / max(1.0, soc_mg_kg)) * 100.0, 2)

        q_co2 = round((basal_respiration_mg_co2_kg_day / 24.0) / max(1.0, microbial_biomass_c_mg_kg), 4)

        stress_status = "Healthy Soil Microflora (Low qCO2 Stress)" if q_co2 <= 0.005 else (
            "Moderate Environmental Stress" if q_co2 <= 0.012 else "High Microbial Stress / Disturbed Ecosystem"
        )

        return {
            "soil_organic_carbon_pct": organic_carbon_pct,
            "microbial_biomass_c_mg_kg": microbial_biomass_c_mg_kg,
            "mbc_to_soc_ratio_pct": mbc_soc_ratio_pct,
            "metabolic_quotient_qco2": q_co2,
            "microbial_stress_evaluation": stress_status,
            "soil_health_insight": "High MBC/SOC ratio (> 2.0%) indicates active biological nutrient recycling capacity."
        }
