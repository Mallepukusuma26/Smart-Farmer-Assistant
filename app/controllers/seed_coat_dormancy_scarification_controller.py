"""
SeedCoatDormancyScarificationEngine Controller.
REST API controllers for Hard Seed Coat Physical Dormancy & Mechanical Scarification.
"""

from flask import jsonify, request
from app.services.agronomy.seed_coat_dormancy_scarification import SeedCoatDormancyScarificationEngine

class SeedCoatDormancyScarificationEngineController:
    """Controller for SeedCoatDormancyScarificationEngine."""

    def __init__(self, service=None):
        self.service = service or SeedCoatDormancyScarificationEngine()

    def compute(self):
        data = request.get_json() or {}
        p1 = float(data.get("param1", 10.0))
        p2 = float(data.get("param2", 5.0))
        p3 = float(data.get("param3", 15.0))
        temp = float(data.get("temp_c", 25.0))
        vwc = float(data.get("vwc", 0.28))

        res = self.service.compute_primary_domain_value(p1, p2, p3, temp, vwc)
        return jsonify({"success": True, "result": res})

    def analyze_grid(self):
        data = request.get_json() or {}
        zones = data.get("zones", [{"zone_id": "ZONE-01", "param1": 10.0, "param2": 5.0}])
        res = self.service.analyze_field_zone_grid(zones)
        return jsonify({"success": True, "result": res})

    def get_report(self):
        farm = request.args.get("farm", "Green Valley Farm")
        field = request.args.get("field", "North Field A1")
        res = self.service.generate_full_agronomic_report(farm, field)
        return jsonify({"success": True, "report": res})
