"""
AgronomyPrecisionFertigationDosingEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_precision_fertigation_dosing import AgronomyPrecisionFertigationDosingEngine

class AgronomyPrecisionFertigationDosingEngineController:
    def __init__(self):
        self.service = AgronomyPrecisionFertigationDosingEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
