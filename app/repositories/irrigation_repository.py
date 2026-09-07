from typing import Optional, List, Dict, Any, Tuple
from datetime import date, datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.irrigation import WaterSource, WaterRequirement, IrrigationSchedule, IrrigationLog, IrrigationAlert
from app.repositories.base_repository import BaseRepository

class IrrigationRepository(BaseRepository[IrrigationSchedule]):
    """Data Access Repository for Water Sources, Irrigation Schedules, Logs, and Deficit Alerts."""

    def __init__(self):
        super().__init__(IrrigationSchedule)

    def create_water_source(self, farm_id: int, name: str, source_type: str = 'Borewell', capacity_liters: float = 50000.0, current_level_pct: float = 80.0, ph_level: Optional[float] = 7.2, salinity_ppm: Optional[float] = 250.0, flow_rate_lpm: Optional[float] = 120.0, notes: Optional[str] = None) -> WaterSource:
        """Register water source for farm."""
        source = WaterSource(
            farm_id=farm_id,
            name=name,
            source_type=source_type,
            capacity_liters=capacity_liters,
            current_level_pct=current_level_pct,
            ph_level=ph_level,
            salinity_ppm=salinity_ppm,
            flow_rate_lpm=flow_rate_lpm,
            notes=notes
        )
        db.session.add(source)
        db.session.commit()
        return source

    def get_water_sources(self, farm_id: int) -> List[WaterSource]:
        """Fetch all water sources belonging to farm."""
        return db.session.query(WaterSource).filter_by(farm_id=farm_id, is_active=True).all()

    def set_water_requirement(self, field_id: int, crop_name: str, growth_stage: str, kc_factor: float, et0_mm_per_day: float, daily_water_need_liters: float, weekly_water_need_liters: float) -> WaterRequirement:
        """Store or update Evapotranspiration water requirement for field plot."""
        req = db.session.query(WaterRequirement).filter_by(field_id=field_id).first()
        if not req:
            req = WaterRequirement(
                field_id=field_id,
                crop_name=crop_name,
                growth_stage=growth_stage,
                kc_factor=kc_factor,
                et0_mm_per_day=et0_mm_per_day,
                daily_water_need_liters=daily_water_need_liters,
                weekly_water_need_liters=weekly_water_need_liters
            )
            db.session.add(req)
        else:
            req.crop_name = crop_name
            req.growth_stage = growth_stage
            req.kc_factor = kc_factor
            req.et0_mm_per_day = et0_mm_per_day
            req.daily_water_need_liters = daily_water_need_liters
            req.weekly_water_need_liters = weekly_water_need_liters
            req.calculated_at = datetime.utcnow()
        db.session.commit()
        return req

    def get_schedules_by_field(self, field_id: int, status: Optional[str] = None) -> List[IrrigationSchedule]:
        """Fetch irrigation schedules for field plot."""
        query = db.session.query(IrrigationSchedule).filter_by(field_id=field_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(IrrigationSchedule.next_irrigation_date.asc()).all()

    def get_due_schedules(self, target_date: Optional[date] = None) -> List[IrrigationSchedule]:
        """Fetch all schedules due on or before target date."""
        if target_date is None:
            target_date = date.today()
        return db.session.query(IrrigationSchedule).filter(
            IrrigationSchedule.next_irrigation_date <= target_date,
            IrrigationSchedule.status == 'Scheduled'
        ).order_by(IrrigationSchedule.priority_level.desc()).all()

    def log_irrigation_event(self, field_id: int, water_used_liters: float, duration_minutes: int = 60, water_source_id: Optional[int] = None, energy_cost_est: float = 0.0, rainfall_observed_mm: float = 0.0, soil_moisture_after_pct: Optional[float] = 45.0, operator_name: Optional[str] = None, notes: Optional[str] = None) -> IrrigationLog:
        """Record completed irrigation event and deduct volume from water source."""
        irr_log = IrrigationLog(
            field_id=field_id,
            water_source_id=water_source_id,
            water_used_liters=water_used_liters,
            duration_minutes=duration_minutes,
            energy_cost_est=energy_cost_est,
            rainfall_observed_mm=rainfall_observed_mm,
            soil_moisture_after_pct=soil_moisture_after_pct,
            operator_name=operator_name,
            notes=notes
        )
        db.session.add(irr_log)

        if water_source_id:
            ws = db.session.get(WaterSource, water_source_id)
            if ws:
                ws.update_level(water_used_liters)

        db.session.commit()
        return irr_log

    def create_alert(self, field_id: int, alert_type: str, severity: str, message: str) -> IrrigationAlert:
        """Create irrigation moisture deficit or pumping alert."""
        alert = IrrigationAlert(
            field_id=field_id,
            alert_type=alert_type,
            severity=severity,
            message=message
        )
        db.session.add(alert)
        db.session.commit()
        return alert

    def get_unresolved_alerts(self, field_id: Optional[int] = None) -> List[IrrigationAlert]:
        """Fetch active unresolved irrigation alerts."""
        query = db.session.query(IrrigationAlert).filter_by(is_resolved=False)
        if field_id:
            query = query.filter_by(field_id=field_id)
        return query.order_by(IrrigationAlert.created_at.desc()).all()

    def get_total_water_consumption(self, field_id: Optional[int] = None, start_date=None, end_date=None) -> float:
        """Calculate total volume of water applied in liters over a date range."""
        query = db.session.query(func.sum(IrrigationLog.water_used_liters))
        if field_id:
            query = query.filter(IrrigationLog.field_id == field_id)
        if start_date:
            query = query.filter(IrrigationLog.irrigation_date >= start_date)
        if end_date:
            query = query.filter(IrrigationLog.irrigation_date <= end_date)
        val = query.scalar()
        return round(float(val), 2) if val else 0.0
