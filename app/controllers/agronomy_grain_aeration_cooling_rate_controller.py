"""
AgronomyGrainAerationCoolingRateEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_grain_aeration_cooling_rate import AgronomyGrainAerationCoolingRateEngine

class AgronomyGrainAerationCoolingRateEngineController:
    def __init__(self):
        self.service = AgronomyGrainAerationCoolingRateEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
