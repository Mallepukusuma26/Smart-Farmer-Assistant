from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.farmer import Farmer, FarmerPreference, FarmerDocument, FarmerActivity, FarmerContact, FarmerNotificationSetting
from app.repositories.base_repository import BaseRepository

class FarmerRepository(BaseRepository[Farmer]):
    """Data Access Repository for Farmer profiles, preferences, documents, and activity streams."""

    def __init__(self):
        super().__init__(Farmer)

    def find_by_user_id(self, user_id: int) -> Optional[Farmer]:
        """Fetch farmer profile linked to specific user ID."""
        return db.session.query(Farmer).filter_by(user_id=user_id).first()

    def find_by_phone(self, phone: str) -> Optional[Farmer]:
        """Fetch farmer profile by phone number."""
        return db.session.query(Farmer).filter_by(phone=phone.strip()).first()

    def get_farmers_by_region(self, region: str) -> List[Farmer]:
        """Get all farmers in a specific geographic agricultural zone/region."""
        return db.session.query(Farmer).filter(func.lower(Farmer.region) == region.lower().strip()).all()

    def get_farmers_by_advisor(self, advisor_id: int) -> List[Farmer]:
        """Get all farmers assigned to a specific agricultural advisor."""
        return db.session.query(Farmer).filter_by(assigned_advisor_id=advisor_id).all()

    def search_farmers(
        self,
        keyword: Optional[str] = None,
        region: Optional[str] = None,
        farming_type: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Farmer], int, int]:
        """Search farmers with keyword filtering across full name, phone, address, and region."""
        query = db.session.query(Farmer)

        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Farmer.full_name.ilike(term),
                    Farmer.phone.ilike(term),
                    Farmer.address.ilike(term),
                    Farmer.main_crop_type.ilike(term)
                )
            )

        if region:
            query = query.filter(Farmer.region == region)

        if farming_type:
            query = query.filter(Farmer.primary_farming_type == farming_type)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(Farmer.full_name.asc()))

    def get_or_create_preferences(self, farmer_id: int) -> FarmerPreference:
        """Fetch or create default preferences configuration for a farmer."""
        pref = db.session.query(FarmerPreference).filter_by(farmer_id=farmer_id).first()
        if not pref:
            pref = FarmerPreference(farmer_id=farmer_id)
            db.session.add(pref)
            db.session.commit()
        return pref

    def update_preferences(self, farmer_id: int, **kwargs) -> FarmerPreference:
        """Update farmer preference settings."""
        pref = self.get_or_create_preferences(farmer_id)
        for key, value in kwargs.items():
            if hasattr(pref, key) and value is not None:
                setattr(pref, key, value)
        db.session.commit()
        return pref

    def add_farmer_document(self, farmer_id: int, document_title: str, document_type: str, file_path: str, file_size_bytes: int = 0, notes: Optional[str] = None) -> FarmerDocument:
        """Upload/record a land title or certificate document for farmer."""
        doc = FarmerDocument(
            farmer_id=farmer_id,
            document_title=document_title,
            document_type=document_type,
            file_path=file_path,
            file_size_bytes=file_size_bytes,
            notes=notes
        )
        db.session.add(doc)
        db.session.commit()
        return doc

    def get_farmer_documents(self, farmer_id: int) -> List[FarmerDocument]:
        """Fetch all documents attached to a farmer profile."""
        return db.session.query(FarmerDocument).filter_by(farmer_id=farmer_id).order_by(FarmerDocument.upload_date.desc()).all()

    def log_activity(self, farmer_id: int, activity_type: str, title: str, description: Optional[str] = None) -> FarmerActivity:
        """Log activity stream event for farmer."""
        activity = FarmerActivity(
            farmer_id=farmer_id,
            activity_type=activity_type,
            title=title,
            description=description
        )
        db.session.add(activity)
        db.session.commit()
        return activity

    def get_recent_activities(self, farmer_id: int, limit: int = 15) -> List[FarmerActivity]:
        """Fetch recent activity timeline entries for a farmer."""
        return db.session.query(FarmerActivity).filter_by(farmer_id=farmer_id).order_by(FarmerActivity.created_at.desc()).limit(limit).all()

    def add_contact(self, farmer_id: int, contact_name: str, phone_number: str, relationship: str = 'Emergency Contact', email: Optional[str] = None) -> FarmerContact:
        """Add emergency contact for farmer."""
        contact = FarmerContact(
            farmer_id=farmer_id,
            contact_name=contact_name,
            phone_number=phone_number,
            relationship=relationship,
            email=email
        )
        db.session.add(contact)
        db.session.commit()
        return contact

    def get_contacts(self, farmer_id: int) -> List[FarmerContact]:
        """Get emergency contacts directory for farmer."""
        return db.session.query(FarmerContact).filter_by(farmer_id=farmer_id).all()
