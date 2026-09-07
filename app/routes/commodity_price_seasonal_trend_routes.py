"""
CommodityPriceSeasonalTrendEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.commodity_price_seasonal_trend_controller import CommodityPriceSeasonalTrendEngineController

commodity_price_seasonal_trend_bp = Blueprint("commodity-price-seasonal-trend", __name__, url_prefix="/api/commodity-price-seasonal-trend")
controller = CommodityPriceSeasonalTrendEngineController()

@commodity_price_seasonal_trend_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@commodity_price_seasonal_trend_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@commodity_price_seasonal_trend_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
