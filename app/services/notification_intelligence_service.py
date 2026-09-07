"""
Notification Intelligence Service Module for Smart Farmer Assistant.

Manages local offline alerts, irrigation schedule reminders, fertilizer application stages,
disease warning alerts, harvest readiness notifications, and financial summary alerts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.extensions import db
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationIntelligenceService:
    """
    Offline notification dispatch engine for generating automated agrarian reminders and priority alerts.
    """

    def __init__(self, repository: Optional[NotificationRepository] = None):
        self.repository = repository or NotificationRepository()

    def generate_irrigation_reminder(self, farmer_id: int, field_name: str, water_m3: float) -> Notification:
        """
        Generates an irrigation alert notification for a specific field plot.
        """
        title = f"Irrigation Scheduled for {field_name}"
        message = f"Apply {water_m3} m³ of water to {field_name} today based on evapotranspiration model."
        return self.repository.create_notification(
            farmer_id=farmer_id,
            title=title,
            message=message,
            category="IRRIGATION",
            priority="HIGH"
        )

    def generate_fertilizer_reminder(self, farmer_id: int, crop_name: str, dose_info: str) -> Notification:
        """
        Generates top-dressing fertilizer reminder notification.
        """
        title = f"Fertilizer Top-Dressing Due for {crop_name}"
        message = f"First top-dressing stage reached: {dose_info}."
        return self.repository.create_notification(
            farmer_id=farmer_id,
            title=title,
            message=message,
            category="FERTILIZER",
            priority="MEDIUM"
        )

    def generate_disease_alert(self, farmer_id: int, field_name: str, disease_name: str, severity_pct: float) -> Notification:
        """
        Generates priority disease outbreak alert notification.
        """
        title = f"Disease Alert: {disease_name} Detected"
        message = f"Lesion analysis on {field_name} indicates {severity_pct}% severity. Review recommended fungicide treatment immediately."
        return self.repository.create_notification(
            farmer_id=farmer_id,
            title=title,
            message=message,
            category="DISEASE",
            priority="URGENT"
        )
