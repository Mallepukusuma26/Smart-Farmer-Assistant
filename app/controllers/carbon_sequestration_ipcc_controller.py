"""
IPCC Tier 2 Soil Organic Carbon Sequestration Engine Controller.
API endpoints for domain calculations and scenario evaluations.
"""

from flask import jsonify, request
from app.services.agronomy.carbon_sequestration_ipcc_engine import IPCCSoilCarbonEngine

class IPCCSoilCarbonEngineController:
    """Controller for IPCCSoilCarbonEngine."""

    def __init__(self, engine=None):
        self.engine = engine or IPCCSoilCarbonEngine()

    def calculate(self):
        data = request.get_json() or {}
        v1 = float(data.get("val1", 5.0))
        v2 = float(data.get("val2", 2.0))
        v3 = float(data.get("val3", 10.0))
        res = self.engine.calculate_primary_metric(v1, v2, v3)
        return jsonify({"success": True, "result": res})

    def evaluate_scenario(self):
        data = request.get_json() or {}
        scenario = data.get("scenario", [={"val1": 4.5, "val2": 2.1}])
        res = self.engine.evaluate_field_scenario(scenario)
        return jsonify({"success": True, "result": res})
