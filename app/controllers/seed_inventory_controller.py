"""
Seed Inventory Controller.
API endpoints for seed sowing rate calculations and inventory tracking.
"""

from flask import jsonify, request
from app.services.seed_inventory_service import SeedInventoryService

class SeedInventoryController:
    """Controller for seed inventory and sowing rate endpoints."""

    def __init__(self, service=None):
        self.service = service or SeedInventoryService()

    def calculate_sowing_rate(self):
        """Calculate sowing rate based on germination and thousand grain weight."""
        data = request.get_json() or {}
        pop = float(data.get("target_population", 250000.0))
        tgw = float(data.get("tgw_g", 40.0))
        germ = float(data.get("germination_pct", 92.0))
        purity = float(data.get("purity_pct", 98.0))

        res = self.service.calculate_sowing_rate(pop, tgw, germ, purity)
        return jsonify({"success": True, "sowing_rate": res})
