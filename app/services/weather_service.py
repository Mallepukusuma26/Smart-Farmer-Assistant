"""
Weather Service Module for Smart Farmer Assistant.

Manages offline manual microclimate logs, Growing Degree Days (GDD),
and Penman-Monteith ET0 reference evapotranspiration math without external API dependency.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.weather_log import WeatherLog
from app.repositories.weather_repository import WeatherRepository
from app.services.irrigation_telemetry_service import IrrigationTelemetryService
from ml.feature_engineering.agronomic_features import AgronomicFeatureEngine
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Business service providing local microclimate weather logging, GDD calculation,
    and ET0 evapotranspiration math.
    """

    def __init__(self, repo: Optional[WeatherRepository] = None):
        self.repo = repo or WeatherRepository()
        self.telemetry_service = IrrigationTelemetryService()
        self.agronomic_engine = AgronomicFeatureEngine()

    def get_logs_by_farm(self, farm_id: int) -> List[WeatherLog]:
        """
        Retrieves microclimate logs for a farm.
        """
        return self.repo.get_by_farm(farm_id)

    def log_weather(self, farm_id: int, data: Dict[str, Any]) -> WeatherLog:
        """
        Registers a new daily microclimate weather observation log.
        """
        max_temp = float(data.get("max_temp_c", 28.0))
        min_temp = float(data.get("min_temp_c", 18.0))
        humidity = float(data.get("avg_humidity_pct", 65.0))
        rainfall = float(data.get("rainfall_mm", 0.0))
        wind = float(data.get("wind_speed_m_s", 2.0))

        gdd = self.agronomic_engine.calculate_gdd(max_temp, min_temp, t_base_c=10.0)
        et0 = self.telemetry_service.calculate_fao_penman_monteith_et0((max_temp + min_temp) / 2.0, humidity, wind)

        log_date_str = data.get("log_date")
        log_date = datetime.strptime(log_date_str, "%Y-%m-%d").date() if log_date_str else datetime.utcnow().date()

        weather = WeatherLog(
            farm_id=farm_id,
            log_date=log_date,
            max_temp_c=max_temp,
            min_temp_c=min_temp,
            avg_humidity_pct=humidity,
            rainfall_mm=rainfall,
            wind_speed_m_s=wind,
            solar_radiation_mj_m2=float(data.get("solar_radiation_mj_m2", 18.0)),
            gdd_calculated=gdd,
            et0_mm_day=et0
        )
        return self.repo.create(weather)
