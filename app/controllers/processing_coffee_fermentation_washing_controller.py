"""
ProcessingCoffeeFermentationWashingEngine Controller.
API controllers for Wet Process Coffee Mucilage Fermentation & Bean Moisture EMC.
"""

from flask import jsonify, request
from app.services.agronomy.processing_coffee_fermentation_washing import ProcessingCoffeeFermentationWashingEngine

class ProcessingCoffeeFermentationWashingEngineController:
    """Controller for ProcessingCoffeeFermentationWashingEngine."""

    def __init__(self, service=None):
        self.service = service or ProcessingCoffeeFermentationWashingEngine()

    def compute(self):
        data = request.get_json() or {}
        v1 = float(data.get("input_1", 12.0))
        v2 = float(data.get("input_2", 6.0))
        v3 = float(data.get("input_3", 10.0))

        res = self.service.calculate_domain_metric(v1, v2, v3)
        return jsonify({"success": True, "result": res})

    def process_grid(self):
        data = request.get_json() or {}
        zones = data.get("zones", [{"v1": 10.0, "v2": 5.0, "v3": 10.0}])
        res = self.service.process_grid_zones(zones)
        return jsonify({"success": True, "result": res})

    def summary(self):
        res = self.service.get_summary_report()
        return jsonify({"success": True, "summary": res})
