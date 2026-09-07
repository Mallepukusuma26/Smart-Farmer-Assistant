from datetime import datetime, date
from typing import Dict, Any, List, Optional
from app.extensions import db

class WaterSource(db.Model):
    """Water source registry for farms (borewell, canal, rainwater pond, river, drip tank)."""
    __tablename__ = 'water_sources'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    source_type = db.Column(db.String(50), nullable=False, default='Borewell') # Borewell, Canal, Pond, River, Rainwater, Tank
    capacity_liters = db.Column(db.Float, nullable=False, default=50000.0)
    current_level_pct = db.Column(db.Float, nullable=False, default=80.0)
    ph_level = db.Column(db.Float, nullable=True, default=7.2)
    salinity_ppm = db.Column(db.Float, nullable=True, default=250.0)
    flow_rate_lpm = db.Column(db.Float, nullable=True, default=120.0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farm = db.relationship('Farm', backref=db.backref('water_sources', lazy='dynamic', cascade='all, delete-orphan'))

    def update_level(self, used_liters: float) -> float:
        """Subtract consumed water volume and update current level percentage."""
        if self.capacity_liters <= 0:
            return 0.0
        used_pct = (used_liters / self.capacity_liters) * 100.0
        self.current_level_pct = max(0.0, min(100.0, self.current_level_pct - used_pct))
        return self.current_level_pct

    def is_water_quality_safe(self) -> bool:
        """Check if water pH and salinity fall within standard agricultural safety limits."""
        ph_ok = (self.ph_level is None) or (6.0 <= self.ph_level <= 8.5)
        sal_ok = (self.salinity_ppm is None) or (self.salinity_ppm <= 1000.0)
        return ph_ok and sal_ok

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'source_type': self.source_type,
            'capacity_liters': self.capacity_liters,
            'current_level_pct': round(self.current_level_pct, 1),
            'ph_level': self.ph_level,
            'salinity_ppm': self.salinity_ppm,
            'flow_rate_lpm': self.flow_rate_lpm,
            'is_active': self.is_active,
            'quality_safe': self.is_water_quality_safe(),
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<WaterSource id={self.id} name='{self.name}' type='{self.source_type}'>"


class WaterRequirement(db.Model):
    """Calculated Evapotranspiration (ET) water requirement benchmarks for fields."""
    __tablename__ = 'water_requirements'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    growth_stage = db.Column(db.String(50), nullable=False, default='Vegetative') # Initial, Vegetative, Flowering, Yield Formation, Ripening
    kc_factor = db.Column(db.Float, nullable=False, default=1.0) # Crop coefficient factor
    et0_mm_per_day = db.Column(db.Float, nullable=False, default=4.5) # Reference evapotranspiration
    daily_water_need_liters = db.Column(db.Float, nullable=False, default=2500.0)
    weekly_water_need_liters = db.Column(db.Float, nullable=False, default=17500.0)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    field = db.relationship('Field', backref=db.backref('water_requirements', lazy='dynamic', cascade='all, delete-orphan'))

    def recalculate_daily_need(self, area_acres: float) -> float:
        """Calculate daily water requirement in liters using FAO Penman-Monteith ETc formula."""
        etc_mm = self.et0_mm_per_day * self.kc_factor
        area_sq_m = area_acres * 4046.86
        self.daily_water_need_liters = round(etc_mm * area_sq_m, 2)
        self.weekly_water_need_liters = round(self.daily_water_need_liters * 7, 2)
        return self.daily_water_need_liters

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_name': self.crop_name,
            'growth_stage': self.growth_stage,
            'kc_factor': self.kc_factor,
            'et0_mm_per_day': self.et0_mm_per_day,
            'daily_water_need_liters': self.daily_water_need_liters,
            'weekly_water_need_liters': self.weekly_water_need_liters,
            'calculated_at': self.calculated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<WaterRequirement id={self.id} crop='{self.crop_name}' daily_liters={self.daily_water_need_liters}>"


class IrrigationSchedule(db.Model):
    """Calculated automated irrigation schedule entity for field management."""
    __tablename__ = 'irrigation_schedules'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('crop_cycles.id', ondelete='SET NULL'), nullable=True)
    water_source_id = db.Column(db.Integer, db.ForeignKey('water_sources.id', ondelete='SET NULL'), nullable=True)
    water_required_liters = db.Column(db.Float, nullable=False, default=1000.0)
    next_irrigation_date = db.Column(db.Date, nullable=False)
    frequency_days = db.Column(db.Integer, default=5)
    duration_minutes = db.Column(db.Integer, default=60)
    method = db.Column(db.String(50), default='Drip') # Drip, Sprinkler, Surface, Sub-irrigation
    status = db.Column(db.String(30), default='Scheduled') # Scheduled, Completed, Skipped, Overdue
    priority_level = db.Column(db.String(20), default='Medium') # Low, Medium, High, Critical
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    water_source = db.relationship('WaterSource', backref=db.backref('schedules', lazy='dynamic'))

    def mark_completed(self) -> None:
        """Mark schedule completed and calculate next target date based on frequency."""
        self.status = 'Completed'
        if self.next_irrigation_date:
            from datetime import timedelta
            self.next_irrigation_date = self.next_irrigation_date + timedelta(days=self.frequency_days)
            self.status = 'Scheduled'

    def is_due_today(self) -> bool:
        """Check if schedule is due today."""
        return self.next_irrigation_date == date.today() and self.status == 'Scheduled'

    def is_overdue(self) -> bool:
        """Check if schedule is past due."""
        return self.next_irrigation_date < date.today() and self.status == 'Scheduled'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_cycle_id': self.crop_cycle_id,
            'water_source_id': self.water_source_id,
            'water_required_liters': self.water_required_liters,
            'next_irrigation_date': self.next_irrigation_date.strftime('%Y-%m-%d') if self.next_irrigation_date else None,
            'frequency_days': self.frequency_days,
            'duration_minutes': self.duration_minutes,
            'method': self.method,
            'status': self.status,
            'priority_level': self.priority_level,
            'is_due_today': self.is_due_today(),
            'is_overdue': self.is_overdue(),
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<IrrigationSchedule id={self.id} field_id={self.field_id} status='{self.status}'>"


class IrrigationLog(db.Model):
    """Historical log of completed irrigation events and water volume tracking."""
    __tablename__ = 'irrigation_logs'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    water_source_id = db.Column(db.Integer, db.ForeignKey('water_sources.id', ondelete='SET NULL'), nullable=True)
    irrigation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    water_used_liters = db.Column(db.Float, nullable=False, default=1000.0)
    duration_minutes = db.Column(db.Integer, default=60)
    energy_cost_est = db.Column(db.Float, default=0.0) # Estimated pumping cost
    rainfall_observed_mm = db.Column(db.Float, default=0.0)
    soil_moisture_after_pct = db.Column(db.Float, nullable=True, default=45.0)
    operator_name = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def calculate_efficiency(self, target_liters: float) -> float:
        """Calculate application efficiency ratio (target volume / actual volume)."""
        if self.water_used_liters <= 0:
            return 0.0
        return round(min(1.0, target_liters / self.water_used_liters) * 100.0, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'water_source_id': self.water_source_id,
            'irrigation_date': self.irrigation_date.strftime('%Y-%m-%d %H:%M'),
            'water_used_liters': self.water_used_liters,
            'duration_minutes': self.duration_minutes,
            'energy_cost_est': self.energy_cost_est,
            'rainfall_observed_mm': self.rainfall_observed_mm,
            'soil_moisture_after_pct': self.soil_moisture_after_pct,
            'operator_name': self.operator_name,
            'notes': self.notes
        }

    def __repr__(self) -> str:
        return f"<IrrigationLog id={self.id} water_used_liters={self.water_used_liters}>"


class IrrigationAlert(db.Model):
    """System-generated alerts for water deficit, over-watering, or maintenance events."""
    __tablename__ = 'irrigation_alerts'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False, default='Moisture Deficit') # Moisture Deficit, Pumping Overload, Water Quality Warning, Schedule Overdue
    severity = db.Column(db.String(20), nullable=False, default='Medium') # Info, Warning, Critical
    message = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    field = db.relationship('Field', backref=db.backref('irrigation_alerts', lazy='dynamic', cascade='all, delete-orphan'))

    def resolve(self) -> None:
        """Mark alert resolved."""
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'is_resolved': self.is_resolved,
            'resolved_at': self.resolved_at.strftime('%Y-%m-%d %H:%M') if self.resolved_at else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<IrrigationAlert id={self.id} type='{self.alert_type}' severity='{self.severity}'>"
