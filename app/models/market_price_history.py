"""
Market Price History SQLAlchemy Model for Smart Farmer Assistant.

Stores historical mandi commodity prices, minimum support prices (MSP),
regional mandi locations, price trends, and trading volumes.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class MarketPriceHistory(db.Model):
    """
    SQLAlchemy model representing a commodity market price observation record.
    """
    __tablename__ = "market_price_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    mandi_location = db.Column(db.String(100), nullable=False, index=True, default="Central Mandi")
    price_date = db.Column(db.Date, nullable=False, index=True)
    modal_price_per_tonne = db.Column(db.Float, nullable=False, default=0.0)
    min_price_per_tonne = db.Column(db.Float, nullable=True, default=0.0)
    max_price_per_tonne = db.Column(db.Float, nullable=True, default=0.0)
    msp_per_tonne = db.Column(db.Float, nullable=True, default=0.0)
    daily_arrival_tonnes = db.Column(db.Float, nullable=True, default=0.0)
    price_trend = db.Column(db.String(20), nullable=False, default="Stable")  # Upward, Downward, Stable

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "crop_name": self.crop_name,
            "mandi_location": self.mandi_location,
            "price_date": self.price_date.strftime("%Y-%m-%d") if self.price_date else None,
            "modal_price_per_tonne": self.modal_price_per_tonne,
            "min_price_per_tonne": self.min_price_per_tonne,
            "max_price_per_tonne": self.max_price_per_tonne,
            "msp_per_tonne": self.msp_per_tonne,
            "daily_arrival_tonnes": self.daily_arrival_tonnes,
            "price_trend": self.price_trend,
            "created_at": self.created_at.isoformat()
        }
