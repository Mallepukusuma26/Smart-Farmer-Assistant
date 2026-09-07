"""
PrecisionAgNitrogenResponseCurveEngine Controller.
REST API controllers for Quadratic-Plateau Nitrogen Response Curve & Economic Optimum Rate.
"""

from flask import jsonify, request
from app.services.agronomy.precision_ag_nitrogen_response_curve_model import PrecisionAgNitrogenResponseCurveEngine

class PrecisionAgNitrogenResponseCurveEngineController:
    """Controller for PrecisionAgNitrogenResponseCurveEngine."""

    def __init__(self, service=None):
        self.service = service or PrecisionAgNitrogenResponseCurveEngine()

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
