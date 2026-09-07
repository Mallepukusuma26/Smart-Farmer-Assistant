"""
AgronomyCropCanopyArchitecture3DEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_crop_canopy_architecture_3d import AgronomyCropCanopyArchitecture3DEngine

class AgronomyCropCanopyArchitecture3DEngineController:
    def __init__(self):
        self.service = AgronomyCropCanopyArchitecture3DEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
