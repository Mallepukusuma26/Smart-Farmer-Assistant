"""
AgriculturalWaterTariffCostEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agricultural_water_tariff_cost_controller import AgriculturalWaterTariffCostEngineController

agricultural_water_tariff_cost_bp = Blueprint("agricultural-water-tariff-cost", __name__, url_prefix="/api/agricultural-water-tariff-cost")
controller = AgriculturalWaterTariffCostEngineController()

@agricultural_water_tariff_cost_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@agricultural_water_tariff_cost_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@agricultural_water_tariff_cost_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
