"""
Weather Log SQLAlchemy Model for Smart Farmer Assistant.

Stores manual local microclimate logs (temperature, humidity, rainfall mm, wind speed, solar radiation)
for Growing Degree Days (GDD) and Penman-Monteith ET0 evapotranspiration math without external API dependency.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class WeatherLog(db.Model):
    """
    SQLAlchemy model representing a local microclimate weather observation log.
    """
    __tablename__ = "weather_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date = db.Column(db.Date, nullable=False, index=True)
    max_temp_c = db.Column(db.Float, nullable=False, default=28.0)
    min_temp_c = db.Column(db.Float, nullable=False, default=18.0)
    avg_humidity_pct = db.Column(db.Float, nullable=False, default=65.0)
    rainfall_mm = db.Column(db.Float, nullable=False, default=0.0)
    wind_speed_m_s = db.Column(db.Float, nullable=True, default=2.0)
    solar_radiation_mj_m2 = db.Column(db.Float, nullable=True, default=18.0)
    gdd_calculated = db.Column(db.Float, nullable=True, default=13.0)
    et0_mm_day = db.Column(db.Float, nullable=True, default=3.5)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    farm = db.relationship("Farm", backref=db.backref("weather_logs", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "log_date": self.log_date.strftime("%Y-%m-%d") if self.log_date else None,
            "max_temp_c": self.max_temp_c,
            "min_temp_c": self.min_temp_c,
            "avg_humidity_pct": self.avg_humidity_pct,
            "rainfall_mm": self.rainfall_mm,
            "wind_speed_m_s": self.wind_speed_m_s,
            "solar_radiation_mj_m2": self.solar_radiation_mj_m2,
            "gdd_calculated": self.gdd_calculated,
            "et0_mm_day": self.et0_mm_day,
            "created_at": self.created_at.isoformat()
        }
