"""
AgronomyGreenhouseMicroclimateVPDEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_greenhouse_microclimate_vpd import AgronomyGreenhouseMicroclimateVPDEngine

class AgronomyGreenhouseMicroclimateVPDEngineController:
    def __init__(self):
        self.service = AgronomyGreenhouseMicroclimateVPDEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
