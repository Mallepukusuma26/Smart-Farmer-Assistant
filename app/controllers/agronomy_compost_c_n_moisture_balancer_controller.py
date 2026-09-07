"""
AgronomyCompostCNMoistureBalancerEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_compost_c_n_moisture_balancer import AgronomyCompostCNMoistureBalancerEngine

class AgronomyCompostCNMoistureBalancerEngineController:
    def __init__(self):
        self.service = AgronomyCompostCNMoistureBalancerEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
