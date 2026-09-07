"""
AgronomyCropWaterProductionFAO33Engine Controller.
"""

from flask import jsonify, request
from app.services.agronomy.agronomy_crop_water_production_fao33 import AgronomyCropWaterProductionFAO33Engine

class AgronomyCropWaterProductionFAO33EngineController:
    def __init__(self, service=None):
        self.service = service or AgronomyCropWaterProductionFAO33Engine()

    def compute(self):
        data = request.get_json() or {}
        v1 = float(data.get("input_1", 10.0))
        v2 = float(data.get("input_2", 5.0))
        v3 = float(data.get("input_3", 10.0))
        return jsonify({"success": True, "result": self.service.compute_metric(v1, v2, v3)})

    def evaluate_grid(self):
        data = request.get_json() or {}
        zones = data.get("zones", [{"v1": 10.0, "v2": 5.0, "v3": 10.0}])
        return jsonify({"success": True, "result": self.service.evaluate_grid(zones)})
