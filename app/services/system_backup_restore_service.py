"""
System Backup & Restore Service Module for Smart Farmer Assistant.

Manages database JSON snapshot export, table schema backups, local backup file archiving,
integrity verification, and dataset restoration.
"""

from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.models.farmer import Farmer
from app.models.farm import Farm
from app.models.field import Field
from app.models.crop import Crop
from app.models.soil import SoilSample
import logging

logger = logging.getLogger(__name__)


class SystemBackupRestoreService:
    """
    Business service creating local offline database JSON snapshots and restore archives.
    """

    def __init__(self, backup_dir: Optional[str] = None):
        self.backup_dir = backup_dir or os.path.join(os.getcwd(), "instance", "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_database_backup(self) -> Dict[str, Any]:
        """
        Exports all platform tables (Users, Farmers, Farms, Fields, Crops, Soil Samples) to JSON snapshot.
        """
        users = User.query.all()
        farmers = Farmer.query.all()
        farms = Farm.query.all()
        fields = Field.query.all()
        crops = Crop.query.all()
        soil_samples = SoilSample.query.all()

        backup_data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_users": len(users),
                "total_farmers": len(farmers),
                "total_farms": len(farms),
                "total_fields": len(fields),
                "total_crops": len(crops),
                "total_soil_samples": len(soil_samples)
            },
            "users": [{"id": u.id, "username": u.username, "email": u.email, "role": u.role.value} for u in users],
            "farmers": [{"id": f.id, "user_id": f.user_id, "farming_type": f.farming_type} for f in farmers],
            "farms": [{"id": fm.id, "farmer_id": fm.farmer_id, "name": fm.name, "area": float(fm.total_area_acres or 0)} for fm in farms],
            "fields": [{"id": fd.id, "farm_id": fd.farm_id, "name": fd.name, "area": float(fd.area_acres or 0)} for fd in fields],
            "crops": [{"id": c.id, "name": c.name, "category": c.category} for c.crops if hasattr(c, "name")] if False else [{"id": c.id, "name": c.name} for c.query.all()] if False else [{"id": c.id, "name": c.name} for c in crops],
            "soil_samples": [{"id": s.id, "field_id": s.field_id, "ph": s.ph_level, "score": s.soil_quality_score} for s in soil_samples]
        }

        filename = f"smart_farmer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.backup_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)

        logger.info(f"Database backup saved to {filepath}")
        return {
            "filename": filename,
            "filepath": filepath,
            "metadata": backup_data["metadata"]
        }
