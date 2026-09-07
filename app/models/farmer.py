from datetime import datetime
from app.extensions import db

class Farmer(db.Model):
    """Primary Farmer profile entity."""
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state_province = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), default='United States')
    region = db.Column(db.String(100), nullable=True, index=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    total_land_area = db.Column(db.Float, default=0.0)
    primary_farming_type = db.Column(db.String(50), default='Crop Farming')  # Crop Farming, Livestock, Mixed, Horticulture
    main_crop_type = db.Column(db.String(50), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    education_level = db.Column(db.String(50), default='High School')
    assigned_advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    farms = db.relationship('Farm', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    revenues = db.relationship('Revenue', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    preferences = db.relationship('FarmerPreference', backref='farmer', uselist=False, cascade='all, delete-orphan')
    documents = db.relationship('FarmerDocument', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('FarmerActivity', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state_province': self.state_province,
            'country': self.country,
            'region': self.region,
            'total_land_area': self.total_land_area,
            'primary_farming_type': self.primary_farming_type,
            'main_crop_type': self.main_crop_type,
            'experience_years': self.experience_years,
            'education_level': self.education_level,
            'assigned_advisor_id': self.assigned_advisor_id,
            'farm_count': self.farms.count(),
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Farmer id={self.id} name='{self.full_name}'>"


class FarmerPreference(db.Model):
    """Farmer system preferences configuration."""
    __tablename__ = 'farmer_preferences'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False, unique=True)
    preferred_unit = db.Column(db.String(20), default='Acres')  # Acres, Hectares, SqMeters
    currency_code = db.Column(db.String(10), default='USD')
    temperature_unit = db.Column(db.String(10), default='C')  # C, F
    enable_irrigation_alerts = db.Column(db.Boolean, default=True)
    enable_disease_alerts = db.Column(db.Boolean, default=True)
    enable_financial_alerts = db.Column(db.Boolean, default=True)
    theme_preference = db.Column(db.String(20), default='emerald')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'preferred_unit': self.preferred_unit,
            'currency_code': self.currency_code,
            'temperature_unit': self.temperature_unit,
            'enable_irrigation_alerts': self.enable_irrigation_alerts,
            'enable_disease_alerts': self.enable_disease_alerts,
            'enable_financial_alerts': self.enable_financial_alerts,
            'theme_preference': self.theme_preference
        }


class FarmerDocument(db.Model):
    """Farmer land titles, soil test certificates, and property documents."""
    __tablename__ = 'farmer_documents'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    document_title = db.Column(db.String(150), nullable=False)
    document_type = db.Column(db.String(50), default='Land Title')  # Land Title, Soil Test, Subsidy, Certificate
    file_path = db.Column(db.String(255), nullable=False)
    file_size_bytes = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'document_title': self.document_title,
            'document_type': self.document_type,
            'file_path': self.file_path,
            'file_size_kb': round(self.file_size_bytes / 1024, 1),
            'upload_date': self.upload_date.strftime('%Y-%m-%d')
        }


class FarmerActivity(db.Model):
    """Activity stream for farmer interactions and task history."""
    __tablename__ = 'farmer_activities'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'activity_type': self.activity_type,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class FarmerContact(db.Model):
    """Emergency and secondary contact directory for farmers."""
    __tablename__ = 'farmer_contacts'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), default='Emergency Contact')
    phone_number = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)

    farmer = db.relationship('Farmer', backref=db.backref('contacts', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'contact_name': self.contact_name,
            'relationship': self.relationship,
            'phone_number': self.phone_number,
            'email': self.email
        }


class FarmerNotificationSetting(db.Model):
    """Specific alert delivery configuration for farmers."""
    __tablename__ = 'farmer_notification_settings'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False, unique=True)
    sms_alerts_enabled = db.Column(db.Boolean, default=True)
    email_summary_enabled = db.Column(db.Boolean, default=True)
    push_notifications_enabled = db.Column(db.Boolean, default=True)

    farmer = db.relationship('Farmer', backref=db.backref('alert_settings', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'sms_alerts_enabled': self.sms_alerts_enabled,
            'email_summary_enabled': self.email_summary_enabled,
            'push_notifications_enabled': self.push_notifications_enabled
        }

