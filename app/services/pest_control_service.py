"""
Integrated Pest Management (IPM) & Pest Control Service Module for Smart Farmer Assistant.

Manages agricultural pest identification, Economic Injury Level (EIL) math,
Economic Threshold (ET) triggers, bio-pesticide dosage calculations,
pre-harvest interval (PHI) safety waiting periods, and spray schedules.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class PestControlService:
    """
    Business service providing Integrated Pest Management (IPM) recommendations,
    Economic Injury Level (EIL) economic math, pesticide dosage per acre,
    and Pre-Harvest Interval (PHI) compliance tracking.
    """

    def __init__(self):
        self.pest_database = {
            "stem borer": {
                "pest_name": "Yellow Stem Borer (Scirpophaga incertulas)",
                "target_crops": ["rice", "sugarcane"],
                "economic_threshold": "5% dead hearts or 1 egg mass / m2",
                "organic_control": "Release Trichogramma japonicum egg parasitoid @ 50,000/ha or install pheromone traps @ 20/ha.",
                "chemical_control": "Chlorantraniliprole 0.4% GR @ 10 kg/ha or Cartap Hydrochloride 4G @ 25 kg/ha.",
                "phi_days": 21,
                "dosage_per_acre_kg": 4.0
            },
            "fall armyworm": {
                "pest_name": "Fall Armyworm (Spodoptera frugiperda)",
                "target_crops": ["maize", "corn", "rice", "sorghum"],
                "economic_threshold": "10% damaged plants in whorl stage",
                "organic_control": "Apply Metarhizium anisopliae or Beauveria bassiana @ 5g/L or Neem oil 1500 ppm @ 5ml/L.",
                "chemical_control": "Emamectin Benzoate 5% SG @ 0.4g/L or Spinetoram 11.7% SC @ 0.5ml/L.",
                "phi_days": 14,
                "dosage_per_acre_kg": 0.1
            },
            "aphids": {
                "pest_name": "Mustard / Cotton Aphid (Aphis gossypii)",
                "target_crops": ["mustard", "cotton", "tomato", "potato", "wheat"],
                "economic_threshold": "20-25 aphids per plant leaf",
                "organic_control": "Spray Verticillium lecanii @ 5g/L or Soapnut solution (1%). Release Chrysoperla carnea predators.",
                "chemical_control": "Imidacloprid 17.8% SL @ 0.3ml/L or Thiamethoxam 25% WG @ 0.2g/L.",
                "phi_days": 7,
                "dosage_per_acre_kg": 0.05
            },
            "whitefly": {
                "pest_name": "Cotton / Vegetable Whitefly (Bemisia tabaci)",
                "target_crops": ["cotton", "tomato", "brinjal", "chili"],
                "economic_threshold": "5-8 whiteflies per leaf",
                "organic_control": "Install yellow sticky traps @ 30/ha or spray Neem formulation @ 5ml/L.",
                "chemical_control": "Pyriproxyfen 10% EC @ 1.5ml/L or Diafenthiuron 50% WP @ 1g/L.",
                "phi_days": 14,
                "dosage_per_acre_kg": 0.25
            }
        }

    def calculate_economic_injury_level(
        self,
        cost_of_control_per_acre: float,
        market_price_per_unit: float,
        yield_per_acre: float,
        damage_coefficient: float = 0.02
    ) -> Dict[str, Any]:
        """
        Calculates Economic Injury Level (EIL) pest density threshold:
        EIL = C / (V * I * D)
        C = Cost of management per area
        V = Market value per unit of yield
        I = Injury per pest density
        D = Damage per unit injury
        """
        value_per_acre = market_price_per_unit * yield_per_acre
        if value_per_acre <= 0 or damage_coefficient <= 0:
            eil_pest_count = 10.0
        else:
            eil_pest_count = cost_of_control_per_acre / (market_price_per_unit * damage_coefficient)

        economic_threshold = eil_pest_count * 0.75  # Action threshold set at 75% of EIL

        return {
            "cost_of_control_per_acre_usd": cost_of_control_per_acre,
            "market_price_per_unit_usd": market_price_per_unit,
            "yield_per_acre": yield_per_acre,
            "economic_injury_level_pests_per_plant": round(eil_pest_count, 2),
            "economic_threshold_action_trigger": round(economic_threshold, 2),
            "recommendation": f"Initiate pest management spray when pest count exceeds {round(economic_threshold, 2)} per plant."
        }

    def get_ipm_recommendation(self, pest_name: str, area_acres: float = 1.0) -> Dict[str, Any]:
        """
        Returns complete IPM protocol, bio-control, chemical dosage, and PHI waiting period.
        """
        name_lower = pest_name.lower().strip()
        info = self.pest_database.get(
            name_lower,
            {
                "pest_name": pest_name,
                "target_crops": ["general"],
                "economic_threshold": "5-10% plant damage",
                "organic_control": "Spray Neem seed kernel extract @ 5% or Azadirachtin 10,000 ppm.",
                "chemical_control": "Broad-spectrum insecticide Chlorpyrifos 20% EC @ 2ml/L.",
                "phi_days": 14,
                "dosage_per_acre_kg": 0.5
            }
        )

        total_dosage_kg = info["dosage_per_acre_kg"] * area_acres

        return {
            "pest_name": info["pest_name"],
            "target_crops": info["target_crops"],
            "economic_threshold": info["economic_threshold"],
            "organic_bio_control": info["organic_control"],
            "chemical_control": info["chemical_control"],
            "pre_harvest_interval_phi_days": info["phi_days"],
            "dosage_per_acre_kg": info["dosage_per_acre_kg"],
            "total_dosage_required_kg": round(total_dosage_kg, 2),
            "safety_warning": f"Observe mandatory {info['phi_days']} days Pre-Harvest Interval (PHI) between final spray and harvest."
        }
