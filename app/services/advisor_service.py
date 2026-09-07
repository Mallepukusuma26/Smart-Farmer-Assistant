from typing import Optional, List, Dict, Any, Tuple
from app.repositories.advisor_repository import AdvisorRepository
from app.models.advisor import Advisor, AdvisorCase, AdvisorConsultation

class AdvisorService:
    """Domain Service for agricultural advisor cases, consultation tickets, and farmer recommendations."""

    def __init__(self, repository: Optional[AdvisorRepository] = None):
        self.repository = repository or AdvisorRepository()

    def open_consultation_case(self, farmer_id: int, advisor_id: int, subject: str, description: str, category: str = 'Crop Health', priority: str = 'Medium', field_id: Optional[int] = None) -> AdvisorCase:
        """Farmer submits advisory request case to an advisor."""
        return self.repository.create_advisory_case(
            advisor_id=advisor_id,
            farmer_id=farmer_id,
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            field_id=field_id
        )

    def respond_to_case(self, case_id: int, sender_role: str, message: str, action_items: Optional[str] = None, resolve_case: bool = False) -> AdvisorConsultation:
        """Add consultation reply or action plan note."""
        consult = self.repository.add_consultation_message(
            case_id=case_id,
            sender_role=sender_role,
            message=message,
            action_items=action_items
        )
        if resolve_case:
            self.repository.update_case_status(case_id, 'Resolved')
        return consult

    def get_farmer_cases(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Fetch all consultation tickets for farmer."""
        cases = self.repository.get_cases_for_farmer(farmer_id)
        return [c.to_dict() for c in cases]

    def get_advisor_dashboard(self, advisor_id: int) -> Dict[str, Any]:
        """Fetch advisor dashboard open cases and assigned farmers statistics."""
        advisor = self.repository.get_by_id(advisor_id)
        if not advisor:
            return {}

        open_cases = self.repository.get_cases_for_advisor(advisor_id, status='Open')
        under_review = self.repository.get_cases_for_advisor(advisor_id, status='Under Review')
        resolved_cases = self.repository.get_cases_for_advisor(advisor_id, status='Resolved')

        return {
            'advisor_profile': advisor.to_dict(),
            'open_cases_count': len(open_cases),
            'under_review_count': len(under_review),
            'resolved_cases_count': len(resolved_cases),
            'open_cases': [c.to_dict() for c in open_cases],
            'average_rating': self.repository.get_advisor_avg_rating(advisor_id)
        }
