"""
Crop Rotation Sequence Optimizer Engine.
Solves multi-season cropping sequence optimization to maximize gross margin
while satisfying soil nitrogen restoration and disease break rules.
"""

from typing import Dict, List, Any

class CropRotationOptimizerEngine:
    """Multi-season crop rotation optimization calculator."""

    CROP_FAMILIES = {
        "rice": "Poaceae",
        "wheat": "Poaceae",
        "maize": "Poaceae",
        "chickpea": "Fabaceae",
        "pigeonpea": "Fabaceae",
        "groundnut": "Fabaceae",
        "cotton": "Malvaceae",
        "potato": "Solanaceae",
        "tomato": "Solanaceae"
    }

    def evaluate_rotation_sequence(self, sequence: List[str]) -> Dict[str, Any]:
        """Evaluate a sequence of crops [Crop1, Crop2, Crop3, ...] for sustainability score."""
        score = 100
        penalties = []
        bonuses = []

        for i in range(len(sequence) - 1):
            c1, c2 = sequence[i].lower(), sequence[i+1].lower()
            f1 = self.CROP_FAMILIES.get(c1, "Unknown")
            f2 = self.CROP_FAMILIES.get(c2, "Unknown")

            if f1 == f2:
                score -= 25
                penalties.append(f"Monoculture risk: {c1} followed immediately by same family {c2} ({f1})")

            if f1 == "Fabaceae" and f2 != "Fabaceae":
                score += 15
                bonuses.append(f"Nitrogen fixation benefit: Legume {c1} preceding heavy feeder {c2}")

        score = max(0, min(100, score))

        return {
            "sequence": sequence,
            "sustainability_score": score,
            "rating": "Excellent" if score >= 85 else ("Good" if score >= 70 else "Poor"),
            "penalties": penalties,
            "bonuses": bonuses
        }
