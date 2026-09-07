"""
Machinery Service Module for Smart Farmer Assistant.

Manages machinery asset inventory, MACRS depreciation, fuel cost tracking, and maintenance schedules.
"""

from typing import Dict, Any, List, Optional, Tuple
from app.models.machinery import Machinery
from app.repositories.machinery_repository import MachineryRepository
import logging

logger = logging.getLogger(__name__)


class MachineryService:
    """
    Business service managing farm machinery assets, maintenance logs, and asset valuation.
    """

    def __init__(self, repo: Optional[MachineryRepository] = None):
        self.repo = repo or MachineryRepository()

    def get_machinery_by_farmer(self, farmer_id: int) -> List[Machinery]:
        """
        Retrieves all machinery assets owned by a farmer.
        """
        return self.repo.get_by_farmer(farmer_id)

    def add_machinery(self, farmer_id: int, data: Dict[str, Any]) -> Machinery:
        """
        Registers a new machinery asset for a farmer.
        """
        purchase_price = float(data.get("purchase_price", 0.0))
        annual_depr = round(purchase_price * 0.1429, 2)  # MACRS 7-yr Year 1
        current_val = round(max(purchase_price - annual_depr, 0.0), 2)

        machinery = Machinery(
            farmer_id=farmer_id,
            name=data.get("name", "Farm Equipment"),
            equipment_type=data.get("equipment_type", "Tractor"),
            model_number=data.get("model_number", "Model-2022"),
            purchase_year=int(data.get("purchase_year", 2022)),
            purchase_price=purchase_price,
            current_valuation=current_val,
            annual_depreciation_usd=annual_depr,
            operating_hours=float(data.get("operating_hours", 0.0)),
            fuel_type=data.get("fuel_type", "Diesel"),
            status="Active"
        )
        return self.repo.create(machinery)
