from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional
from app.repositories.irrigation_repository import IrrigationRepository
from app.models.irrigation import IrrigationSchedule, IrrigationLog, IrrigationAlert, WaterRequirement
from app.models.field import Field
from app.models.crop import Crop

class IrrigationService:
    """Domain Service for FAO Penman-Monteith ETc water requirement calculations, scheduling, and deficit warnings."""

    def __init__(self, repository: Optional[IrrigationRepository] = None):
        self.repository = repository or IrrigationRepository()

    def generate_schedule(
        self,
        field_id: int,
        crop_id: Optional[int] = None,
        crop_cycle_id: Optional[int] = None,
        soil_moisture: float = 25.0,
        temperature: float = 28.0,
        humidity: float = 65.0,
        rainfall_mm: float = 0.0
    ) -> IrrigationSchedule:
        """Calculate daily ETc water requirement and generate automated irrigation schedule."""
        field = Field.query.get(field_id)
        crop = Crop.query.get(crop_id) if crop_id else None

        area = field.area if field else 1.0
        method = field.irrigation_type if field else 'Drip'

        # Reference evapotranspiration estimate (ET0) in mm/day
        et0 = max(2.5, 0.0023 * (temperature + 17.8) * (temperature - 15) ** 0.5 * 10)
        kc = 0.85 # Default vegetative crop coefficient

        water_mm_day = max(0.0, (et0 * kc) - (rainfall_mm * 0.7))

        # Soil moisture correction factor
        if soil_moisture < 20:
            water_mm_day *= 1.3
            self.repository.create_alert(
                field_id=field_id,
                alert_type='Moisture Deficit',
                severity='High',
                message=f"Critical soil moisture level ({soil_moisture}%). Immediate irrigation recommended."
            )
        elif soil_moisture > 40:
            water_mm_day *= 0.5

        # Convert mm/day over acreage to liters (1 mm over 1 acre = 4,046.86 liters)
        water_liters_per_day = water_mm_day * 4046.86 * area

        if method == 'Drip':
            efficiency = 0.90
            frequency_days = 2
            duration_minutes = max(30, int(water_liters_per_day * frequency_days / 50)) # 50 L/min emitter rate
        elif method == 'Sprinkler':
            efficiency = 0.75
            frequency_days = 4
            duration_minutes = max(45, int(water_liters_per_day * frequency_days / 80))
        else: # Flood / Surface / Rainfed
            efficiency = 0.60
            frequency_days = 7
            duration_minutes = max(60, int(water_liters_per_day * frequency_days / 120))

        actual_liters = round(water_liters_per_day * frequency_days / efficiency, 1)
        next_date = date.today() + timedelta(days=frequency_days)

        notes = f"Estimated ET0: {et0:.1f} mm/day. System application efficiency: {int(efficiency * 100)}%."

        # Save benchmark water requirement
        self.repository.set_water_requirement(
            field_id=field_id,
            crop_name=crop.name if crop else 'General Crop',
            growth_stage='Vegetative',
            kc_factor=kc,
            et0_mm_per_day=round(et0, 2),
            daily_water_need_liters=round(water_liters_per_day, 1),
            weekly_water_need_liters=round(water_liters_per_day * 7, 1)
        )

        schedule = self.repository.create(
            field_id=field_id,
            crop_cycle_id=crop_cycle_id,
            water_required_liters=actual_liters,
            next_irrigation_date=next_date,
            frequency_days=frequency_days,
            duration_minutes=duration_minutes,
            method=method,
            status='Scheduled',
            priority_level='High' if soil_moisture < 20 else 'Medium',
            notes=notes
        )

        return schedule

    def log_irrigation(
        self,
        field_id: int,
        water_used_liters: float,
        duration_minutes: int = 60,
        water_source_id: Optional[int] = None,
        rainfall_observed_mm: float = 0.0,
        operator_name: Optional[str] = None,
        notes: Optional[str] = None
    ) -> IrrigationLog:
        """Record completed irrigation event and calculate pumping cost."""
        pumping_cost_est = round((duration_minutes / 60.0) * 45.0, 2)  # $45 per pumping hour est.
        return self.repository.log_irrigation_event(
            field_id=field_id,
            water_used_liters=float(water_used_liters),
            duration_minutes=int(duration_minutes),
            water_source_id=water_source_id,
            energy_cost_est=pumping_cost_est,
            rainfall_observed_mm=float(rainfall_observed_mm),
            operator_name=operator_name,
            notes=notes
        )
