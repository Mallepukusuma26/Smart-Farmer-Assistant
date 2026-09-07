"""
Harvest Log SQLAlchemy Model for Smart Farmer Assistant.

Stores crop harvest records, total harvested yield (tonnes), moisture content %,
grain quality grade, warehouse storage location, and sales transaction status.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class HarvestLog(db.Model):
    """
    SQLAlchemy model representing a completed crop harvest batch and warehouse storage record.
    """
    __tablename__ = "harvest_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True)
    field_id = db.Column(db.Integer, db.ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    harvest_date = db.Column(db.Date, nullable=False)
    yield_tonnes = db.Column(db.Float, nullable=False, default=0.0)
    moisture_content_pct = db.Column(db.Float, nullable=True, default=14.0)
    quality_grade = db.Column(db.String(20), nullable=True, default="Grade A")
    warehouse_location = db.Column(db.String(100), nullable=True)
    storage_status = db.Column(db.String(30), nullable=False, default="In Storage")  # In Storage, Sold, Processing
    total_sales_revenue_usd = db.Column(db.Float, nullable=True, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farmer = db.relationship("Farmer", backref=db.backref("harvest_logs", lazy="dynamic"))
    field = db.relationship("Field", backref=db.backref("harvest_logs", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "field_id": self.field_id,
            "crop_name": self.crop_name,
            "harvest_date": self.harvest_date.strftime("%Y-%m-%d") if self.harvest_date else None,
            "yield_tonnes": self.yield_tonnes,
            "moisture_content_pct": self.moisture_content_pct,
            "quality_grade": self.quality_grade,
            "warehouse_location": self.warehouse_location,
            "storage_status": self.storage_status,
            "total_sales_revenue_usd": self.total_sales_revenue_usd,
            "created_at": self.created_at.isoformat()
        }
