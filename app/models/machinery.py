"""
Machinery SQLAlchemy Model for Smart Farmer Assistant.

Stores farm machinery and equipment inventory records (Tractor, Harvester, Seeder, Spray Rig, Tubewell Pump),
purchase valuation, MACRS 7-year depreciation, engine operating hours, and maintenance schedules.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class Machinery(db.Model):
    """
    SQLAlchemy model representing a piece of farm machinery asset.
    """
    __tablename__ = "machinery"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    equipment_type = db.Column(db.String(50), nullable=False)  # Tractor, Harvester, Seeder, Sprayer, Pump
    model_number = db.Column(db.String(50), nullable=True)
    purchase_year = db.Column(db.Integer, nullable=True, default=2022)
    purchase_price = db.Column(db.Float, nullable=False, default=0.0)
    current_valuation = db.Column(db.Float, nullable=True, default=0.0)
    annual_depreciation_usd = db.Column(db.Float, nullable=True, default=0.0)
    operating_hours = db.Column(db.Float, nullable=True, default=0.0)
    fuel_type = db.Column(db.String(30), nullable=True, default="Diesel")
    last_maintenance_date = db.Column(db.Date, nullable=True)
    next_maintenance_due = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="Active")  # Active, Under Maintenance, Retired

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farmer = db.relationship("Farmer", backref=db.backref("machinery_assets", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "name": self.name,
            "equipment_type": self.equipment_type,
            "model_number": self.model_number,
            "purchase_year": self.purchase_year,
            "purchase_price": self.purchase_price,
            "current_valuation": self.current_valuation,
            "annual_depreciation_usd": self.annual_depreciation_usd,
            "operating_hours": self.operating_hours,
            "fuel_type": self.fuel_type,
            "last_maintenance_date": self.last_maintenance_date.strftime("%Y-%m-%d") if self.last_maintenance_date else None,
            "next_maintenance_due": self.next_maintenance_due.strftime("%Y-%m-%d") if self.next_maintenance_due else None,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
