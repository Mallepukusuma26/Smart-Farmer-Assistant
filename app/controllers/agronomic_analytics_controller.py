"""
Agronomic Analytics Controller.
API endpoints for regional yield benchmarking and field performance statistics.
"""

from flask import jsonify, request
from app.services.agronomic_analytics_service import AgronomicAnalyticsService

class AgronomicAnalyticsController:
    """Controller for agronomic analytics endpoints."""

    def __init__(self, service=None):
        self.service = service or AgronomicAnalyticsService()

    def benchmark_yield(self, field_id: int):
        """Benchmark field yield against regional standards."""
        yield_val = float(request.args.get("actual_yield", 4.2))
        crop = request.args.get("crop", "wheat")
        res = self.service.benchmark_field_yield(field_id, yield_val, crop)
        return jsonify({"success": True, "benchmark": res})
