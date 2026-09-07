from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.report import Report, ScheduledReport, ReportExport
from app.repositories.base_repository import BaseRepository

class ReportRepository(BaseRepository[Report]):
    """Data Access Repository for PDF/CSV Report Generation History, Schedules, and Downloads."""

    def __init__(self):
        super().__init__(Report)

    def save_report(self, farmer_id: int, report_type: str, title: str, file_path: str, file_format: str = 'pdf', file_size_kb: float = 0.0, farm_id: Optional[int] = None, parameters: Optional[str] = None) -> Report:
        """Register generated report output file."""
        rep = Report(
            farmer_id=farmer_id,
            farm_id=farm_id,
            report_type=report_type,
            title=title,
            file_path=file_path,
            file_format=file_format,
            file_size_kb=file_size_kb,
            parameters_used=parameters
        )
        db.session.add(rep)
        db.session.commit()
        return rep

    def get_reports_by_farmer(self, farmer_id: int, report_type: Optional[str] = None) -> List[Report]:
        """Fetch all reports generated for a farmer."""
        query = db.session.query(Report).filter_by(farmer_id=farmer_id)
        if report_type:
            query = query.filter_by(report_type=report_type)
        return query.order_by(Report.created_at.desc()).all()

    def log_report_export(self, report_id: int, user_id: int, ip_address: Optional[str] = None) -> ReportExport:
        """Log report download audit event."""
        exp = ReportExport(
            report_id=report_id,
            user_id=user_id,
            ip_address=ip_address
        )
        db.session.add(exp)
        db.session.commit()
        return exp
