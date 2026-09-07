"""
Pest Economic Threshold Controller.
API endpoints for insect pest Economic Injury Level (EIL) calculations.
"""

from flask import jsonify, request
from app.services.agronomy.pest_population_degree_day_engine import PestPopulationDegreeDayEngine

class PestEconomicThresholdController:
    """Controller for pest economic threshold endpoints."""

    def __init__(self, engine=None):
        self.engine = engine or PestPopulationDegreeDayEngine()

    def calculate_eil(self):
        """Calculate EIL and economic threshold for pest control action."""
        data = request.get_json() or {}
        cost = float(data.get("control_cost_ha", 45.0))
        price = float(data.get("market_price_ton", 220.0))
        loss = float(data.get("yield_loss_per_pest", 0.05))

        res = self.engine.calculate_economic_injury_level(cost, price, loss)
        return jsonify({"success": True, "eil_calculation": res})
