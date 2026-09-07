"""
Water Source SQLAlchemy Model for Smart Farmer Assistant.

Stores farm water source records (Tubewell, Irrigation Canal, Storage Pond, Rainwater Harvesting Tank),
pumping capacity (Liters/Minute), water quality pH/EC, and reservoir water level tracking.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class WaterSource(db.Model):
    """
    SQLAlchemy model representing a farm water resource asset.
    """
    __tablename__ = "water_sources"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    source_name = db.Column(db.String(100), nullable=False, index=True)
    source_type = db.Column(db.String(50), nullable=False)  # Tubewell, Canal, Pond, Rainwater Tank
    capacity_liters = db.Column(db.Float, nullable=True, default=0.0)
    current_water_level_pct = db.Column(db.Float, nullable=True, default=100.0)
    flow_rate_lpm = db.Column(db.Float, nullable=True, default=250.0)
    water_ph = db.Column(db.Float, nullable=True, default=7.0)
    water_ec_ds_m = db.Column(db.Float, nullable=True, default=0.8)
    status = db.Column(db.String(30), nullable=False, default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farm = db.relationship("Farm", backref=db.backref("water_sources", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "capacity_liters": self.capacity_liters,
            "current_water_level_pct": self.current_water_level_pct,
            "flow_rate_lpm": self.flow_rate_lpm,
            "water_ph": self.water_ph,
            "water_ec_ds_m": self.water_ec_ds_m,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
