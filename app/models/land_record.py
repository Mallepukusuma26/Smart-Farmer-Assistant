"""
Land Record SQLAlchemy Model for Smart Farmer Assistant.

Stores farm plot cadastral survey numbers, GPS boundary coordinates, land ownership deeds,
soil classification records, topography slope ratings, and boundary survey metadata.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class LandRecord(db.Model):
    """
    SQLAlchemy model representing official land ownership survey records and plot boundary polygons.
    """
    __tablename__ = "land_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    survey_number = db.Column(db.String(50), nullable=False, index=True)
    subdivision_number = db.Column(db.String(50), nullable=True)
    deed_owner_name = db.Column(db.String(150), nullable=False)
    land_area_acres = db.Column(db.Float, nullable=False, default=1.0)
    land_area_hectares = db.Column(db.Float, nullable=True, default=0.4047)
    soil_classification = db.Column(db.String(50), nullable=True, default="Loam")
    slope_gradient_pct = db.Column(db.Float, nullable=True, default=2.0)
    elevation_above_sea_level_m = db.Column(db.Float, nullable=True, default=150.0)
    boundary_coordinates_json = db.Column(db.Text, nullable=True)  # Polygon coordinates
    is_irrigation_equipped = db.Column(db.Boolean, default=True, nullable=False)
    registration_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farm = db.relationship("Farm", backref=db.backref("land_records", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "survey_number": self.survey_number,
            "subdivision_number": self.subdivision_number,
            "deed_owner_name": self.deed_owner_name,
            "land_area_acres": self.land_area_acres,
            "land_area_hectares": self.land_area_hectares,
            "soil_classification": self.soil_classification,
            "slope_gradient_pct": self.slope_gradient_pct,
            "elevation_above_sea_level_m": self.elevation_above_sea_level_m,
            "boundary_coordinates_json": self.boundary_coordinates_json,
            "is_irrigation_equipped": self.is_irrigation_equipped,
            "registration_date": self.registration_date.strftime("%Y-%m-%d") if self.registration_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
