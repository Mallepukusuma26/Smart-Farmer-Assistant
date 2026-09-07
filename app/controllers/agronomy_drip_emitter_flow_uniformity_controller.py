"""
AgronomyDripEmitterFlowUniformityEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_drip_emitter_flow_uniformity import AgronomyDripEmitterFlowUniformityEngine

class AgronomyDripEmitterFlowUniformityEngineController:
    def __init__(self):
        self.service = AgronomyDripEmitterFlowUniformityEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
