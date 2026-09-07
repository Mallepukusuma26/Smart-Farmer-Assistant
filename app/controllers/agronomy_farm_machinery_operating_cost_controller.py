"""
AgronomyFarmMachineryOperatingCostEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_farm_machinery_operating_cost import AgronomyFarmMachineryOperatingCostEngine

class AgronomyFarmMachineryOperatingCostEngineController:
    def __init__(self):
        self.service = AgronomyFarmMachineryOperatingCostEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
