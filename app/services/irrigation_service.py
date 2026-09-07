from datetime import datetime, timedelta
from app.extensions import db
from app.models.irrigation import IrrigationSchedule, IrrigationLog
from app.models.field import Field
from app.models.crop import Crop, CropCycle

class IrrigationService:
    """Service layer for offline irrigation scheduling and water usage logging."""

    @staticmethod
    def generate_schedule(field_id, crop_id=None, crop_cycle_id=None, soil_moisture=25.0, temperature=28.0, humidity=65.0, rainfall_mm=0.0):
        """Calculate daily water requirement and generate irrigation schedule."""
        field = Field.query.get(field_id)
        crop = Crop.query.get(crop_id) if crop_id else None

        area = field.area if field else 1.0
        method = field.irrigation_type if field else 'Drip'

        # Reference evapotranspiration estimate (ET0) in mm/day
        et0 = max(2.5, 0.0023 * (temperature + 17.8) * (temperature - 15) ** 0.5 * 10)
        kc = 0.85 # Crop coefficient default

        water_mm_day = max(0.0, (et0 * kc) - (rainfall_mm * 0.7))
        
        # Adjust for soil moisture
        if soil_moisture < 20:
            water_mm_day *= 1.3
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
        else: # Flood / Rainfed
            efficiency = 0.60
            frequency_days = 7
            duration_minutes = max(60, int(water_liters_per_day * frequency_days / 120))

        actual_liters = round(water_liters_per_day * frequency_days / efficiency, 1)
        next_date = (datetime.utcnow() + timedelta(days=frequency_days)).date()

        notes = f"Estimated ET0: {et0:.1f} mm/day. System efficiency factor: {int(efficiency*100)}%."

        schedule = IrrigationSchedule(
            field_id=field_id,
            crop_cycle_id=crop_cycle_id,
            water_required_liters=actual_liters,
            next_irrigation_date=next_date,
            frequency_days=frequency_days,
            duration_minutes=duration_minutes,
            method=method,
            status='Scheduled',
            notes=notes
        )

        db.session.add(schedule)
        db.session.commit()
        return schedule

    @staticmethod
    def log_irrigation(field_id, water_used_liters, duration_minutes, rainfall_observed_mm=0.0, notes=None):
        """Log completed irrigation activity."""
        log = IrrigationLog(
            field_id=field_id,
            irrigation_date=datetime.utcnow(),
            water_used_liters=float(water_used_liters),
            duration_minutes=int(duration_minutes),
            rainfall_observed_mm=float(rainfall_observed_mm),
            notes=notes
        )
        db.session.add(log)
        db.session.commit()
        return log
