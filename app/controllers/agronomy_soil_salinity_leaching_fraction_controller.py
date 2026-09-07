"""
AgronomySoilSalinityLeachingFractionEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_soil_salinity_leaching_fraction import AgronomySoilSalinityLeachingFractionEngine

class AgronomySoilSalinityLeachingFractionEngineController:
    def __init__(self):
        self.service = AgronomySoilSalinityLeachingFractionEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
