from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.advisor import Advisor, AdvisorCase, AdvisorConsultation, AdvisorReview, AdvisorSpecialization
from app.repositories.base_repository import BaseRepository

class AdvisorRepository(BaseRepository[Advisor]):
    """Data Access Repository for Agricultural Advisor profiles, consultation cases, and reviews."""

    def __init__(self):
        super().__init__(Advisor)

    def find_by_user_id(self, user_id: int) -> Optional[Advisor]:
        """Fetch advisor profile linked to specific user ID."""
        return db.session.query(Advisor).filter_by(user_id=user_id).first()

    def get_available_advisors(self, region: Optional[str] = None, specialization: Optional[str] = None) -> List[Advisor]:
        """Fetch active/available advisors by region or specialization."""
        query = db.session.query(Advisor).filter(Advisor.is_available == True)
        if region:
            query = query.filter(func.lower(Advisor.region) == region.lower().strip())
        if specialization:
            query = query.filter(Advisor.specialization.ilike(f"%{specialization}%"))
        return query.all()

    def create_advisory_case(self, advisor_id: int, farmer_id: int, subject: str, description: str, category: str = 'Crop Health', priority: str = 'Medium', field_id: Optional[int] = None) -> AdvisorCase:
        """Create new advisory consultation ticket/case."""
        case = AdvisorCase(
            advisor_id=advisor_id,
            farmer_id=farmer_id,
            field_id=field_id,
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            status='Open'
        )
        db.session.add(case)
        db.session.commit()
        return case

    def get_cases_for_farmer(self, farmer_id: int, status: Optional[str] = None) -> List[AdvisorCase]:
        """Get all consultation cases opened by a farmer."""
        query = db.session.query(AdvisorCase).filter_by(farmer_id=farmer_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(AdvisorCase.created_at.desc()).all()

    def get_cases_for_advisor(self, advisor_id: int, status: Optional[str] = None) -> List[AdvisorCase]:
        """Get all consultation cases assigned to an advisor."""
        query = db.session.query(AdvisorCase).filter_by(advisor_id=advisor_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(AdvisorCase.created_at.desc()).all()

    def add_consultation_message(self, case_id: int, sender_role: str, message: str, action_items: Optional[str] = None) -> AdvisorConsultation:
        """Add reply/recommendation note inside an advisory case."""
        consult = AdvisorConsultation(
            case_id=case_id,
            sender_role=sender_role.upper(),
            message=message,
            action_items=action_items
        )
        db.session.add(consult)
        db.session.commit()
        return consult

    def update_case_status(self, case_id: int, status: str) -> Optional[AdvisorCase]:
        """Update case status (Open, Under Review, Resolved, Closed)."""
        case = db.session.get(AdvisorCase, case_id)
        if case:
            case.status = status
            if status in ['Resolved', 'Closed']:
                from datetime import datetime
                case.resolved_at = datetime.utcnow()
            db.session.commit()
        return case

    def add_review(self, advisor_id: int, farmer_id: int, rating: int, comments: Optional[str] = None) -> AdvisorReview:
        """Post review rating for an advisor."""
        review = AdvisorReview(
            advisor_id=advisor_id,
            farmer_id=farmer_id,
            rating=max(1, min(5, rating)),
            comments=comments
        )
        db.session.add(review)
        db.session.commit()
        return review

    def get_advisor_avg_rating(self, advisor_id: int) -> float:
        """Calculate average rating for an advisor."""
        result = db.session.query(func.avg(AdvisorReview.rating)).filter_by(advisor_id=advisor_id).scalar()
        return round(float(result), 1) if result else 5.0
