"""
Harvest Log Service Module for Smart Farmer Assistant.

Manages harvest yield records, grain moisture shrinkage math, and warehouse storage status.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.harvest_log import HarvestLog
from app.repositories.harvest_repository import HarvestRepository
from app.services.harvest_analytics_service import HarvestAnalyticsService
import logging

logger = logging.getLogger(__name__)


class HarvestLogService:
    """
    Business service managing harvest batch records, moisture shrinkage, and warehouse logs.
    """

    def __init__(self, repo: Optional[HarvestRepository] = None):
        self.repo = repo or HarvestRepository()
        self.analytics_service = HarvestAnalyticsService()

    def get_logs_by_farmer(self, farmer_id: int) -> List[HarvestLog]:
        """
        Retrieves harvest logs for a farmer.
        """
        return self.repo.get_by_farmer(farmer_id)

    def log_harvest(self, farmer_id: int, data: Dict[str, Any]) -> HarvestLog:
        """
        Registers a completed crop harvest batch log.
        """
        yield_tonnes = float(data.get("yield_tonnes", 10.0))
        moisture_pct = float(data.get("moisture_content_pct", 14.0))

        # Calculate moisture shrinkage if moisture > 14%
        shrinkage = self.analytics_service.calculate_moisture_shrinkage(
            initial_weight_kg=yield_tonnes * 1000.0,
            initial_moisture_pct=moisture_pct,
            target_moisture_pct=14.0
        )

        final_yield_tonnes = shrinkage["final_weight_after_drying_kg"] / 1000.0

        h_date_str = data.get("harvest_date")
        harvest_date = datetime.strptime(h_date_str, "%Y-%m-%d").date() if h_date_str else datetime.utcnow().date()

        harvest = HarvestLog(
            farmer_id=farmer_id,
            field_id=data.get("field_id", type=int) if isinstance(data.get("field_id"), int) else None,
            crop_name=data.get("crop_name", "rice"),
            harvest_date=harvest_date,
            yield_tonnes=final_yield_tonnes,
            moisture_content_pct=moisture_pct,
            quality_grade=data.get("quality_grade", "Grade A"),
            warehouse_location=data.get("warehouse_location", "Farm Warehouse #1"),
            storage_status="In Storage",
            total_sales_revenue_usd=float(data.get("total_sales_revenue_usd", 0.0))
        )
        return self.repo.create(harvest)
