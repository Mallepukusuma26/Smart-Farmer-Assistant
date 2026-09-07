"""
Water Source Service Module for Smart Farmer Assistant.

Manages tubewell, canal, pond, and rainwater tank water resource assets.
"""

from typing import Dict, Any, List, Optional
from app.models.water_source import WaterSource
from app.repositories.water_source_repository import WaterSourceRepository
import logging

logger = logging.getLogger(__name__)


class WaterSourceService:
    """
    Business service managing farm water resources and reservoir levels.
    """

    def __init__(self, repo: Optional[WaterSourceRepository] = None):
        self.repo = repo or WaterSourceRepository()

    def get_sources_by_farm(self, farm_id: int) -> List[WaterSource]:
        """
        Retrieves water sources associated with a farm.
        """
        return self.repo.get_by_farm(farm_id)

    def add_water_source(self, farm_id: int, data: Dict[str, Any]) -> WaterSource:
        """
        Registers a new water resource for a farm.
        """
        source = WaterSource(
            farm_id=farm_id,
            source_name=data.get("source_name", "Tubewell #1"),
            source_type=data.get("source_type", "Tubewell"),
            capacity_liters=float(data.get("capacity_liters", 100000.0)),
            current_water_level_pct=float(data.get("current_water_level_pct", 100.0)),
            flow_rate_lpm=float(data.get("flow_rate_lpm", 250.0)),
            water_ph=float(data.get("water_ph", 7.0)),
            water_ec_ds_m=float(data.get("water_ec_ds_m", 0.8)),
            status="Active"
        )
        return self.repo.create(source)
