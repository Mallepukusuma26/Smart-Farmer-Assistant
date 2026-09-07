from typing import Dict, Any, Optional
from sqlalchemy import func
from app.extensions import db
from app.models.user import User
from app.models.farmer import Farmer
from app.models.farm import Farm
from app.models.field import Field
from app.models.crop import Crop
from app.models.soil import SoilRecord
from app.models.disease import DiseaseDetection
from app.models.finance import Expense, Revenue
from app.models.irrigation import IrrigationSchedule, IrrigationLog

class DashboardService:
    """Domain Service for computing aggregate KPIs and chart trends for Admin and Farmer Dashboards."""

    @staticmethod
    def get_admin_dashboard_stats() -> Dict[str, Any]:
        """Compute aggregate system metrics for Administrator dashboard."""
        total_users = db.session.query(func.count(User.id)).scalar() or 0
        total_farmers = db.session.query(func.count(Farmer.id)).scalar() or 0
        total_farms = db.session.query(func.count(Farm.id)).scalar() or 0
        total_fields = db.session.query(func.count(Field.id)).scalar() or 0
        total_crops = db.session.query(func.count(Crop.id)).scalar() or 0
        total_disease_scans = db.session.query(func.count(DiseaseDetection.id)).scalar() or 0
        total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0.0
        total_revenue = db.session.query(func.sum(Revenue.total_revenue)).scalar() or 0.0

        avg_soil_health = db.session.query(func.avg(SoilRecord.health_score)).scalar() or 75.0

        return {
            'kpis': {
                'total_users': total_users,
                'total_farmers': total_farmers,
                'total_farms': total_farms,
                'total_fields': total_fields,
                'total_crops': total_crops,
                'total_disease_scans': total_disease_scans,
                'total_expenses': round(float(total_expenses), 2),
                'total_revenue': round(float(total_revenue), 2),
                'total_net_profit': round(float(total_revenue - total_expenses), 2),
                'average_soil_health_score': round(float(avg_soil_health), 1)
            }
        }

    @staticmethod
    def get_farmer_dashboard_kpis(farmer_id: int) -> Dict[str, Any]:
        """Compute specific operational KPIs and monthly trends for a farmer."""
        farmer = Farmer.query.get(farmer_id)
        if not farmer:
            return {}

        farms = db.session.query(Farm).filter_by(farmer_id=farmer_id).all()
        farm_ids = [f.id for f in farms]

        fields = db.session.query(Field).filter(Field.farm_id.in_(farm_ids)).all() if farm_ids else []
        field_ids = [fl.id for fl in fields]

        total_land_area = sum([f.total_area for f in farms]) if farms else farmer.total_land_area

        total_expenses = db.session.query(func.sum(Expense.amount)).filter_by(farmer_id=farmer_id).scalar() or 0.0
        total_revenue = db.session.query(func.sum(Revenue.total_revenue)).filter_by(farmer_id=farmer_id).scalar() or 0.0
        net_profit = total_revenue - total_expenses

        disease_cases = db.session.query(func.count(DiseaseDetection.id)).filter_by(farmer_id=farmer_id).scalar() or 0
        pending_schedules = db.session.query(func.count(IrrigationSchedule.id)).filter(
            IrrigationSchedule.field_id.in_(field_ids),
            IrrigationSchedule.status == 'Scheduled'
        ).scalar() if field_ids else 0

        avg_soil = db.session.query(func.avg(SoilRecord.health_score)).filter(
            SoilRecord.field_id.in_(field_ids)
        ).scalar() if field_ids else 75.0

        return {
            'summary': {
                'total_farms': len(farms),
                'total_fields': len(fields),
                'total_land_acres': round(total_land_area, 2),
                'total_expenses': round(float(total_expenses), 2),
                'total_revenue': round(float(total_revenue), 2),
                'net_profit': round(float(net_profit), 2),
                'disease_cases_count': disease_cases,
                'pending_irrigation_count': pending_schedules,
                'avg_soil_score': round(float(avg_soil or 75.0), 1)
            }
        }
