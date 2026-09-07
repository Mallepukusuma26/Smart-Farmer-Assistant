"""
Crop Disease Treatment Service Module for Smart Farmer Assistant.

Provides pathogen life cycle modeling, organic & synthetic chemical spray schedules,
fungicide FRAC code rotation rules, and disease prevention protocol generation.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class CropDiseaseTreatmentService:
    """
    Business service providing disease treatment schedules, fungicide FRAC code rotation
    to prevent pathogen resistance, and organic bio-fungicide options.
    """

    def __init__(self):
        self.disease_db = {
            "rice brown spot": {
                "pathogen": "Bipolaris oryzae (Fungus)",
                "organic_treatment": "Spray Neem seed kernel extract (NSKE 5%) or Pseudomonas fluorescens @ 10g/L.",
                "chemical_treatment": "Mancozeb 75% WP @ 2g/L or Propiconazole 25% EC @ 1ml/L.",
                "frac_code": "FRAC 3 (DMI / Triazole)",
                "spray_interval_days": 10,
                "prevention": "Use certified disease-free seeds, balance Nitrogen application, maintain field sanitation."
            },
            "potato late blight": {
                "pathogen": "Phytophthora infestans (Oomycete)",
                "organic_treatment": "Copper Oxychloride 50% WP @ 3g/L or Bordeaux Mixture (1%).",
                "chemical_treatment": "Cymoxanil + Mancozeb @ 2g/L or Metalaxyl + Mancozeb @ 2.5g/L.",
                "frac_code": "FRAC 4 (Phenylamides) / FRAC M03",
                "spray_interval_days": 7,
                "prevention": "Destroy infected tubers, destroy volunteer plants, maintain wide row spacing."
            },
            "tomato early blight": {
                "pathogen": "Alternaria solani (Fungus)",
                "organic_treatment": "Trichoderma viride @ 5g/L or Copper Hydroxide @ 2g/L.",
                "chemical_treatment": "Azoxystrobin 23% SC @ 1ml/L or Difenoconazole 25% EC @ 0.5ml/L.",
                "frac_code": "FRAC 11 (QoI / Strobilurin)",
                "spray_interval_days": 10,
                "prevention": "Mulch soil surface to prevent spore splash, remove lower infected leaves."
            },
            "corn common rust": {
                "pathogen": "Puccinia sorghi (Fungus)",
                "organic_treatment": "Sulfur 80% WP @ 3g/L or Bacillus subtilis @ 5g/L.",
                "chemical_treatment": "Tebuconazole 25.9% EC @ 1ml/L or Pyraclostrobin @ 1.5ml/L.",
                "frac_code": "FRAC 3 / FRAC 11",
                "spray_interval_days": 14,
                "prevention": "Plant resistant hybrids, clear crop residue post-harvest."
            }
        }

    def get_treatment_protocol(self, disease_name: str, severity_level: str = "moderate") -> Dict[str, Any]:
        """
        Retrieves detailed organic, chemical, FRAC code, and spray schedule recommendations.
        """
        name_lower = disease_name.lower().strip()
        info = self.disease_db.get(
            name_lower,
            {
                "pathogen": "Fungal / Bacterial Pathogen",
                "organic_treatment": "Spray Neem oil 10,000 ppm @ 3ml/L or Bio-fungicide Trichoderma.",
                "chemical_treatment": "Broad-spectrum fungicide Mancozeb 75% WP @ 2g/L.",
                "frac_code": "FRAC M03 (Multi-site)",
                "spray_interval_days": 10,
                "prevention": "Improve field drainage, avoid overhead irrigation, rotate crops."
            }
        )

        interval = info["spray_interval_days"]
        if severity_level.lower() == "high" or severity_level.lower() == "severe":
            interval = max(5, interval - 3)

        return {
            "disease_name": disease_name,
            "pathogen": info["pathogen"],
            "severity_level": severity_level,
            "organic_treatment": info["organic_treatment"],
            "chemical_treatment": info["chemical_treatment"],
            "frac_code": info["frac_code"],
            "recommended_spray_interval_days": interval,
            "fungicide_rotation_rule": "Alternate FRAC code active ingredients every 2 sprays to avoid pathogen resistance.",
            "prevention_guidelines": info["prevention"]
        }
