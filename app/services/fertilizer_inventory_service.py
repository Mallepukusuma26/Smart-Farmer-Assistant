"""
Fertilizer Inventory Service Module for Smart Farmer Assistant.

Manages farm fertilizer warehouse stock records, reorder point threshold alerts,
NPK content valuation, purchase history logging, and safety handling recommendations.
"""

from typing import Dict, Any, List, Optional, Tuple
from app.models.fertilizer import Fertilizer
from app.repositories.fertilizer_repository import FertilizerRepository
import logging

logger = logging.getLogger(__name__)


class FertilizerInventoryService:
    """
    Business service managing fertilizer stock levels, inventory reorder alerts,
    purchase expense tracking, and material safety guidelines.
    """

    def __init__(self, fert_repo: Optional[FertilizerRepository] = None):
        self.fert_repo = fert_repo or FertilizerRepository()

    def get_inventory_status(self) -> Dict[str, Any]:
        """
        Retrieves global fertilizer inventory levels, total stock weight (kg),
        total monetary valuation, and identifies items below reorder thresholds.
        """
        fertilizers = self.fert_repo.get_all()
        total_items = len(fertilizers)
        total_stock_kg = 0.0
        total_valuation_usd = 0.0
        low_stock_items = []

        for f in fertilizers:
            stock = float(f.stock_quantity_kg or 0.0)
            cost = float(f.cost_per_kg or 0.0)
            total_stock_kg += stock
            total_valuation_usd += stock * cost

            # Reorder threshold check (default 50 kg)
            if stock < 50.0:
                low_stock_items.append({
                    "id": f.id,
                    "name": f.name,
                    "type": f.type,
                    "current_stock_kg": stock,
                    "reorder_recommended_kg": 200.0 - stock
                })

        return {
            "total_fertilizer_types": total_items,
            "total_stock_kg": round(total_stock_kg, 2),
            "total_valuation_usd": round(total_valuation_usd, 2),
            "low_stock_alerts_count": len(low_stock_items),
            "low_stock_items": low_stock_items
        }

    def record_stock_purchase(
        self,
        fertilizer_id: int,
        quantity_kg: float,
        unit_cost: float,
        purchase_date: Optional[str] = None
    ) -> Optional[Fertilizer]:
        """
        Updates fertilizer warehouse inventory stock quantity and unit cost.
        """
        fertilizer = self.fert_repo.get_by_id(fertilizer_id)
        if not fertilizer:
            logger.error(f"Fertilizer ID {fertilizer_id} not found")
            return None

        current_stock = float(fertilizer.stock_quantity_kg or 0.0)
        new_stock = current_stock + quantity_kg
        fertilizer.stock_quantity_kg = new_stock
        fertilizer.cost_per_kg = unit_cost

        return self.fert_repo.update(fertilizer)

    def deduct_usage_stock(self, fertilizer_id: int, quantity_kg: float) -> Tuple[bool, str]:
        """
        Deducts applied fertilizer quantity from warehouse stock following application.
        """
        fertilizer = self.fert_repo.get_by_id(fertilizer_id)
        if not fertilizer:
            return False, "Fertilizer not found"

        current_stock = float(fertilizer.stock_quantity_kg or 0.0)
        if current_stock < quantity_kg:
            return False, f"Insufficient stock: requested {quantity_kg} kg but only {current_stock} kg available"

        fertilizer.stock_quantity_kg = current_stock - quantity_kg
        self.fert_repo.update(fertilizer)
        return True, "Stock deducted successfully"
