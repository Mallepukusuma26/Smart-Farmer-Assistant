"""
Crop Water Stress Index Controller.
API endpoints for thermal canopy temperature water stress evaluation.
"""

from flask import jsonify, request
from app.services.agronomy.crop_water_stress_index_engine import CropWaterStressIndexEngine

class CropWaterStressController:
    """Controller for CWSI evaluation endpoints."""

    def __init__(self, engine=None):
        self.engine = engine or CropWaterStressIndexEngine()

    def evaluate_stress(self):
        """API endpoint to calculate CWSI from thermal sensor readings."""
        data = request.get_json() or {}
        tc = float(data.get("canopy_temp", 28.5))
        ta = float(data.get("air_temp", 26.0))
        rh = float(data.get("rh_pct", 55.0))

        res = self.engine.calculate_cwsi(tc, ta, rh)
        return jsonify({"success": True, "cwsi_evaluation": res})
