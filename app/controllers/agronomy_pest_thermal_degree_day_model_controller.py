"""
AgronomyPestThermalDegreeDayModelEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_pest_thermal_degree_day_model import AgronomyPestThermalDegreeDayModelEngine

class AgronomyPestThermalDegreeDayModelEngineController:
    def __init__(self):
        self.service = AgronomyPestThermalDegreeDayModelEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
