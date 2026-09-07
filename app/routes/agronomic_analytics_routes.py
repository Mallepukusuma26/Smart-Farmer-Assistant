"""
Agronomic Analytics Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomic_analytics_controller import AgronomicAnalyticsController

agronomic_analytics_bp = Blueprint("agronomic_analytics", __name__, url_prefix="/api/agronomic-analytics")
controller = AgronomicAnalyticsController()

@agronomic_analytics_bp.route("/fields/<int:field_id>/benchmark", methods=["GET"])
def benchmark(field_id: int):
    return controller.benchmark_yield(field_id)
