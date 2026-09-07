"""
AgronomySubsurfaceTileDrainageDepthEngine Controller.
"""
from flask import jsonify, request
from app.services.agronomy.agronomy_subsurface_tile_drainage_depth import AgronomySubsurfaceTileDrainageDepthEngine

class AgronomySubsurfaceTileDrainageDepthEngineController:
    def __init__(self):
        self.service = AgronomySubsurfaceTileDrainageDepthEngine()
    def compute(self):
        d = request.get_json() or {}
        return jsonify({"success": True, "result": self.service.compute(float(d.get("v1", 10.0)), float(d.get("v2", 5.0)))})
