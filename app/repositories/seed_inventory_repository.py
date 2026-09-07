"""
Seed Inventory Repository.
Data access layer for seed lot batches and stock inventory.
"""

from typing import List, Dict, Any

class SeedInventoryRepository:
    """Repository for seed lots and germination records."""

    def get_seed_lots(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Retrieve farmer seed lot inventory."""
        return [
            {"lot_id": "LOT-WHT-2026", "crop": "Wheat", "variety": "HD-2967", "quantity_kg": 250.0, "germination_pct": 94.0},
            {"lot_id": "LOT-MZE-2026", "crop": "Maize", "variety": "Pioneer-3396", "quantity_kg": 100.0, "germination_pct": 96.0}
        ]
