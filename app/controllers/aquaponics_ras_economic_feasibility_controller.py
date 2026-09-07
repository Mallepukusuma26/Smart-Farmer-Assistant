"""
AquaponicsRASEconomicFeasibilityEngine Controller.
REST API controllers for CapEx OpEx Net Present Value (NPV) Aquaponics Feasibility.
"""

from flask import jsonify, request
from app.services.agronomy.aquaponics_ras_economic_feasibility import AquaponicsRASEconomicFeasibilityEngine

class AquaponicsRASEconomicFeasibilityEngineController:
    """Controller for AquaponicsRASEconomicFeasibilityEngine."""

    def __init__(self, service=None):
        self.service = service or AquaponicsRASEconomicFeasibilityEngine()

    def compute_metric(self):
        """API endpoint to compute core metric."""
        data = request.get_json() or {}
        v1 = float(data.get("val1", 12.0))
        v2 = float(data.get("val2", 6.5))
        v3 = float(data.get("val3", 4.0))
        res = self.service.compute_core_metric(v1, v2, v3)
        return jsonify({"success": True, "result": res})

    def run_simulation(self):
        """API endpoint to execute multi-zone spatial simulation."""
        data = request.get_json() or {}
        zones = data.get("zones", [{"v1": 12.0, "v2": 6.5, "v3": 4.0}])
        res = self.service.execute_multi_zone_simulation(zones)
        return jsonify({"success": True, "result": res})

    def calibrate(self):
        """API endpoint to calibrate parameters."""
        data = request.get_json() or {}
        obs = data.get("observations", [10.5, 12.0, 9.8, 11.2])
        res = self.service.calibrate_engine_parameters(obs)
        return jsonify({"success": True, "result": res})
