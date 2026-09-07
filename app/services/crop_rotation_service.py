"""
Crop Rotation Service Module for Smart Farmer Assistant.

Provides crop rotation sequence optimization, leguminous soil nitrogen fixing calculations,
disease cycle disruption rules, soil structure preservation guidelines, and multi-year rotation plans.
"""

from typing import Dict, Any, List, Optional, Tuple
from app.models.crop import Crop
from app.models.field import Field
from app.models.soil import SoilSample
from app.repositories.crop_repository import CropRepository
from app.repositories.field_repository import FieldRepository
import logging

logger = logging.getLogger(__name__)


class CropRotationService:
    """
    Business service calculating optimal crop rotation sequences based on botanical family rules,
    nutrient extraction balances, soil nitrogen replenishment, and pest cycle suppression.
    """

    def __init__(self, crop_repo: Optional[CropRepository] = None, field_repo: Optional[FieldRepository] = None):
        self.crop_repo = crop_repo or CropRepository()
        self.field_repo = field_repo or FieldRepository()

    def get_botanical_family(self, crop_name: str) -> str:
        """
        Maps crop name to its botanical plant family for rotation disease prevention.
        """
        crop_lower = crop_name.lower().strip()
        families = {
            "tomato": "Solanaceae (Nightshade)",
            "potato": "Solanaceae (Nightshade)",
            "eggplant": "Solanaceae (Nightshade)",
            "pepper": "Solanaceae (Nightshade)",
            "chili": "Solanaceae (Nightshade)",
            "wheat": "Poaceae (Grass)",
            "rice": "Poaceae (Grass)",
            "maize": "Poaceae (Grass)",
            "corn": "Poaceae (Grass)",
            "barley": "Poaceae (Grass)",
            "oats": "Poaceae (Grass)",
            "sugarcane": "Poaceae (Grass)",
            "soybean": "Fabaceae (Legume)",
            "groundnut": "Fabaceae (Legume)",
            "peanut": "Fabaceae (Legume)",
            "chickpea": "Fabaceae (Legume)",
            "lentil": "Fabaceae (Legume)",
            "pea": "Fabaceae (Legume)",
            "beans": "Fabaceae (Legume)",
            "cotton": "Malvaceae (Mallow)",
            "mustard": "Brassicaceae (Mustard)",
            "cabbage": "Brassicaceae (Mustard)",
            "cauliflower": "Brassicaceae (Mustard)",
            "sunflower": "Asteraceae (Daisy)",
            "onion": "Amaryllidaceae (Onion)",
            "garlic": "Amaryllidaceae (Onion)"
        }
        return families.get(crop_lower, "General Agricultural Crop")

    def calculate_nitrogen_fixation(self, legume_crop: str, area_acres: float) -> Dict[str, Any]:
        """
        Calculates bio-available nitrogen fixed by leguminous crops per acre.
        """
        crop_lower = legume_crop.lower().strip()
        fixation_rates = {
            "soybean": 45.0,  # kg N/acre
            "groundnut": 50.0,
            "peanut": 50.0,
            "chickpea": 35.0,
            "lentil": 30.0,
            "pea": 40.0,
            "beans": 35.0,
            "clover": 65.0,
            "alfalfa": 80.0
        }
        rate_per_acre = fixation_rates.get(crop_lower, 25.0)
        total_fixed_kg = rate_per_acre * area_acres

        return {
            "legume_crop": legume_crop,
            "area_acres": area_acres,
            "nitrogen_fixed_per_acre_kg": rate_per_acre,
            "total_nitrogen_fixed_kg": total_fixed_kg,
            "fertilizer_equivalent_urea_kg": round(total_fixed_kg * 2.17, 2),  # 46% N in Urea
            "estimated_cost_savings_usd": round(total_fixed_kg * 1.5, 2)
        }

    def recommend_rotation_sequence(self, current_crop_name: str, field_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Generates a 3-year optimal crop rotation sequence to maintain soil fertility and suppress pests.
        """
        family = self.get_botanical_family(current_crop_name)
        current_lower = current_crop_name.lower().strip()

        # Rotation rule matrices
        if "solanaceae" in family.lower():
            next_year_1 = ["Legumes (Soybean / Chickpea)", "Gramineae (Maize / Wheat)"]
            next_year_2 = ["Brassica (Mustard / Cabbage)", "Root Vegetables"]
            next_year_3 = ["Solanaceae (Tomato / Potato - Safe Return)"]
            reasoning = "High risk of Soil-borne Fungal pathogens (Early Blight / Fusarium). Rotate out of Solanaceae for 2 full years."
        elif "fabaceae" in family.lower() or "legume" in family.lower():
            next_year_1 = ["Heavy Nitrogen Feeders (Maize / Wheat / Cotton)"]
            next_year_2 = ["Leafy Vegetables / Brassica"]
            next_year_3 = ["Legumes (Soybean / Groundnut - Safe Return)"]
            reasoning = "Soil is enriched with fixed Nitrogen from previous Legume crop. Ideal for heavy nitrogen-consuming cereal crops."
        elif "poaceae" in family.lower() or "grass" in family.lower():
            next_year_1 = ["Nitrogen Fixing Legumes (Soybean / Groundnut / Chickpea)"]
            next_year_2 = ["Deep Rooted Oilseeds (Sunflower / Mustard)"]
            next_year_3 = ["Cereals (Wheat / Rice / Maize - Safe Return)"]
            reasoning = "Cereals deplete soil Nitrogen and Organic Matter. Follow with Legumes to replenish soil nutrients."
        else:
            next_year_1 = ["Leguminous Pulse Crops"]
            next_year_2 = ["Cereal Grains"]
            next_year_3 = ["Commercial Cash Crops"]
            reasoning = "Standard 3-year balanced rotation sequence to preserve soil structure."

        return {
            "current_crop": current_crop_name,
            "current_family": family,
            "rotation_plan": {
                "year_1_recommendation": next_year_1,
                "year_2_recommendation": next_year_2,
                "year_3_recommendation": next_year_3
            },
            "agronomic_reasoning": reasoning,
            "expected_soil_health_benefit": "Improves organic matter, prevents soil-borne pathogen cycles, and reduces synthetic NPK requirements."
        }
