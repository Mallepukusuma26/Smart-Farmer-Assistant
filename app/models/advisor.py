from datetime import datetime
from app.extensions import db

class Advisor(db.Model):
    """Agricultural Advisor profile entity."""
    __tablename__ = 'advisors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False, index=True)
    qualification = db.Column(db.String(100), nullable=True)
    specialization = db.Column(db.String(100), nullable=True, index=True)
    license_number = db.Column(db.String(50), nullable=True)
    years_experience = db.Column(db.Integer, default=5)
    organization = db.Column(db.String(150), default='Agricultural Extension Services')
    region = db.Column(db.String(100), nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assigned_farmers = db.relationship('Farmer', backref='assigned_advisor', lazy='dynamic')
    advisor_cases = db.relationship('AdvisorCase', backref='advisor', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'qualification': self.qualification,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'years_experience': self.years_experience,
            'organization': self.organization,
            'region': self.region,
            'phone': self.phone,
            'bio': self.bio,
            'is_available': self.is_available,
            'assigned_farmers_count': self.assigned_farmers.count(),
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Advisor id={self.id} name='{self.full_name}'>"


class AdvisorCase(db.Model):
    """Advisory consultation case opened by or assigned to a farmer."""
    __tablename__ = 'advisor_cases'

    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id', ondelete='CASCADE'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    subject = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), default='Crop Health')  # Soil, Crop, Fertilizer, Disease, Water, Yield
    priority = db.Column(db.String(20), default='Medium')      # Low, Medium, High, Urgent
    status = db.Column(db.String(30), default='Open')           # Open, Under Review, Resolved, Closed
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    consultations = db.relationship('AdvisorConsultation', backref='case', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'advisor_id': self.advisor_id,
            'farmer_id': self.farmer_id,
            'field_id': self.field_id,
            'subject': self.subject,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'resolved_at': self.resolved_at.strftime('%Y-%m-%d %H:%M') if self.resolved_at else None
        }


class AdvisorConsultation(db.Model):
    """Consultation message/recommendation entry within an AdvisorCase."""
    __tablename__ = 'advisor_consultations'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('advisor_cases.id', ondelete='CASCADE'), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)  # ADVISOR, FARMER
    message = db.Column(db.Text, nullable=False)
    action_items = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'sender_role': self.sender_role,
            'message': self.message,
            'action_items': self.action_items,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class AdvisorReview(db.Model):
    """Farmer feedback rating for advisory consultations."""
    __tablename__ = 'advisor_reviews'

    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id', ondelete='CASCADE'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5) # 1-5 stars
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    advisor = db.relationship('Advisor', backref=db.backref('reviews', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'advisor_id': self.advisor_id,
            'farmer_id': self.farmer_id,
            'rating': self.rating,
            'comments': self.comments,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class AdvisorSpecialization(db.Model):
    """Expertise tags for matching advisors with specific crop or soil issues."""
    __tablename__ = 'advisor_specializations'

    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id', ondelete='CASCADE'), nullable=False)
    domain = db.Column(db.String(50), nullable=False) # Pest Control, Soil Health, Drip Irrigation, Crop Disease
    certified_level = db.Column(db.String(30), default='Senior Specialist')

    advisor = db.relationship('Advisor', backref=db.backref('specializations', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'advisor_id': self.advisor_id,
            'domain': self.domain,
            'certified_level': self.certified_level
        }

