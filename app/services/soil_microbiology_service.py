"""
Soil Microbiology & Biological Health Service Module for Smart Farmer Assistant.

Calculates soil microbial biomass carbon and nitrogen (MBC/MBN) ratios,
arbuscular mycorrhizal fungi (AMF) root colonization percentages,
enzyme activity indices (dehydrogenase, alkaline phosphatase, urease),
and biological soil health quality scoring.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class SoilMicrobiologyService:
    """
    Business service evaluating biological soil fertility, microbial biomass C:N ratio,
    enzyme activity, and soil biological health index (SBHI).
    """

    @staticmethod
    def calculate_microbial_biomass_cn(
        microbial_carbon_mg_kg: float,
        microbial_nitrogen_mg_kg: float
    ) -> Dict[str, Any]:
        """
        Calculates soil microbial biomass C:N ratio (optimal range 8:1 to 12:1).
        """
        if microbial_nitrogen_mg_kg <= 0:
            cn_ratio = 10.0
        else:
            cn_ratio = microbial_carbon_mg_kg / microbial_nitrogen_mg_kg

        cn_ratio = round(cn_ratio, 2)

        if 8.0 <= cn_ratio <= 12.0:
            status = "Optimal Fungal:Bacterial Balance"
            advice = "Soil food web is well-balanced. Maintain organic matter inputs."
        elif cn_ratio < 8.0:
            status = "Bacterial Dominated Soil"
            advice = "Incorporate woody/high-carbon organic residues (straw, woodchips) to encourage fungal biomass."
        else:
            status = "Fungal Dominated / High Carbon Soil"
            advice = "Incorporate leguminous green manure to lower C:N ratio towards optimal balance."

        return {
            "microbial_carbon_mg_kg": microbial_carbon_mg_kg,
            "microbial_nitrogen_mg_kg": microbial_nitrogen_mg_kg,
            "microbial_cn_ratio": cn_ratio,
            "biological_status": status,
            "management_advice": advice
        }

    @staticmethod
    def evaluate_soil_enzymes(
        dehydrogenase_ug_tpf_g_24h: float,
        phosphatase_ug_pnp_g_h: float,
        urease_ug_nh4_g_2h: float
    ) -> Dict[str, Any]:
        """
        Evaluates soil extracellular enzyme activity metrics indicating microbial metabolic capacity.
        """
        # Dehydrogenase: indicator of total viable microbial respiration
        dh_status = "High Activity" if dehydrogenase_ug_tpf_g_24h >= 50.0 else "Low Biological Activity"

        # Phosphatase: indicator of organic P mineralization
        ph_status = "High P Mineralization" if phosphatase_ug_pnp_g_h >= 100.0 else "Low P Mineralization"

        # Urease: indicator of Nitrogen hydrolytic capacity
        ur_status = "High Urease Capacity" if urease_ug_nh4_g_2h >= 25.0 else "Low Urease Activity"

        overall_score = 0
        if dehydrogenase_ug_tpf_g_24h >= 50.0: overall_score += 35
        if phosphatase_ug_pnp_g_h >= 100.0: overall_score += 35
        if urease_ug_nh4_g_2h >= 25.0: overall_score += 30

        return {
            "dehydrogenase_activity": {"value": dehydrogenase_ug_tpf_g_24h, "status": dh_status},
            "phosphatase_activity": {"value": phosphatase_ug_pnp_g_h, "status": ph_status},
            "urease_activity": {"value": urease_ug_nh4_g_2h, "status": ur_status},
            "enzyme_activity_score": overall_score,
            "biological_rating": "Vigorous Biological Soil Health" if overall_score >= 70 else "Depressed Microbial Activity"
        }
