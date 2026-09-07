"""
Pest Record SQLAlchemy Model for Smart Farmer Assistant.

Stores field pest observation logs, pest species identification, Economic Threshold (ET) status,
applied IPM bio/chemical controls, pre-harvest interval (PHI) dates, and control efficacy ratings.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class PestRecord(db.Model):
    """
    SQLAlchemy model representing a field pest incidence observation and IPM control log.
    """
    __tablename__ = "pest_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True)
    field_id = db.Column(db.Integer, db.ForeignKey("fields.id", ondelete="CASCADE"), nullable=True, index=True)
    pest_name = db.Column(db.String(100), nullable=False, index=True)
    scientific_name = db.Column(db.String(150), nullable=True)
    pest_count_per_plant = db.Column(db.Float, nullable=True, default=0.0)
    economic_threshold_exceeded = db.Column(db.Boolean, default=False, nullable=False)
    control_type_applied = db.Column(db.String(50), nullable=True)  # Organic, Chemical, Biological, Mechanical
    pesticide_name = db.Column(db.String(100), nullable=True)
    dosage_per_acre_kg = db.Column(db.Float, nullable=True, default=0.0)
    total_quantity_applied = db.Column(db.Float, nullable=True, default=0.0)
    phi_days = db.Column(db.Integer, nullable=True, default=14)
    safe_harvest_date = db.Column(db.Date, nullable=True)
    control_efficacy_pct = db.Column(db.Float, nullable=True, default=85.0)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farmer = db.relationship("Farmer", backref=db.backref("pest_records", lazy="dynamic"))
    field = db.relationship("Field", backref=db.backref("pest_records", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "field_id": self.field_id,
            "pest_name": self.pest_name,
            "scientific_name": self.scientific_name,
            "pest_count_per_plant": self.pest_count_per_plant,
            "economic_threshold_exceeded": self.economic_threshold_exceeded,
            "control_type_applied": self.control_type_applied,
            "pesticide_name": self.pesticide_name,
            "dosage_per_acre_kg": self.dosage_per_acre_kg,
            "total_quantity_applied": self.total_quantity_applied,
            "phi_days": self.phi_days,
            "safe_harvest_date": self.safe_harvest_date.strftime("%Y-%m-%d") if self.safe_harvest_date else None,
            "control_efficacy_pct": self.control_efficacy_pct,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
