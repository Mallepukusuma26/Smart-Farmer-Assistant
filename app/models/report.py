from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class Report(db.Model):
    """Generated PDF / CSV / HTML / JSON reports registry entity."""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='SET NULL'), nullable=True)
    report_type = db.Column(db.String(50), nullable=False) # Farmer, Farm, Field, Soil, Crop Recommendation, Fertilizer, Irrigation, Disease, Yield, Financial, Monthly, Seasonal, Annual
    title = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_format = db.Column(db.String(10), default='pdf') # pdf, csv, json, html
    file_size_kb = db.Column(db.Float, default=0.0)
    parameters_used = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'report_type': self.report_type,
            'title': self.title,
            'file_path': self.file_path,
            'file_format': self.file_format,
            'file_size_kb': round(self.file_size_kb, 1),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<Report id={self.id} title='{self.title}'>"


class ScheduledReport(db.Model):
    """Automated recurring report schedule setup."""
    __tablename__ = 'scheduled_reports'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(20), default='Monthly') # Weekly, Monthly, Seasonal
    preferred_format = db.Column(db.String(10), default='pdf')
    last_generated_at = db.Column(db.DateTime, nullable=True)
    next_scheduled_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    farmer = db.relationship('Farmer', backref=db.backref('scheduled_reports', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'report_type': self.report_type,
            'frequency': self.frequency,
            'preferred_format': self.preferred_format,
            'last_generated_at': self.last_generated_at.strftime('%Y-%m-%d %H:%M') if self.last_generated_at else None,
            'next_scheduled_at': self.next_scheduled_at.strftime('%Y-%m-%d %H:%M'),
            'is_active': self.is_active
        }


class ReportExport(db.Model):
    """Audit log of user report downloads and exports."""
    __tablename__ = 'report_exports'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    exported_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)

    report = db.relationship('Report', backref=db.backref('exports', lazy='dynamic', cascade='all, delete-orphan'))
    user = db.relationship('User')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'report_id': self.report_id,
            'user_id': self.user_id,
            'exported_at': self.exported_at.strftime('%Y-%m-%d %H:%M'),
            'ip_address': self.ip_address
        }

