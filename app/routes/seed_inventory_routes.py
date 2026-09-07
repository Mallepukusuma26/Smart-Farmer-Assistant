"""
Seed Inventory Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_inventory_controller import SeedInventoryController

seed_inventory_bp = Blueprint("seed_inventory", __name__, url_prefix="/api/seed-inventory")
controller = SeedInventoryController()

@seed_inventory_bp.route("/calculate-sowing-rate", methods=["POST"])
def calculate_rate():
    return controller.calculate_sowing_rate()
