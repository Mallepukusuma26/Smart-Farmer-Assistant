"""
AgronomySprinklerApplicationIntensityEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_sprinkler_application_intensity import AgronomySprinklerApplicationIntensityEngine

class AgronomySprinklerApplicationIntensityEngineController:
    def __init__(self):
        self.service = AgronomySprinklerApplicationIntensityEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
