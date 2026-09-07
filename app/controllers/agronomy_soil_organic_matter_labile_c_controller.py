"""
AgronomySoilOrganicMatterLabileCEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_soil_organic_matter_labile_c import AgronomySoilOrganicMatterLabileCEngine

class AgronomySoilOrganicMatterLabileCEngineController:
    def __init__(self):
        self.service = AgronomySoilOrganicMatterLabileCEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
