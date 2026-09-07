from datetime import datetime
from app.extensions import db

class Farm(db.Model):
    """Farm property entity belonging to a Farmer."""
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(150), nullable=False)
    county_district = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    total_area = db.Column(db.Float, nullable=False, default=1.0)
    unit = db.Column(db.String(20), default='Acres', nullable=False)
    ownership_type = db.Column(db.String(30), default='Owned')  # Owned, Leased, Rented, Shared
    default_soil_type = db.Column(db.String(50), default='Loamy')
    water_source_primary = db.Column(db.String(50), default='Well Water')  # Well, Canal, River, Rainfed
    elevation_meters = db.Column(db.Float, default=100.0)
    slope_percentage = db.Column(db.Float, default=2.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    fields = db.relationship('Field', backref='farm', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='farm', lazy='dynamic')
    revenues = db.relationship('Revenue', backref='farm', lazy='dynamic')
    documents = db.relationship('FarmDocument', backref='farm', lazy='dynamic', cascade='all, delete-orphan')
    location_details = db.relationship('FarmLocation', backref='farm', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'name': self.name,
            'location': self.location,
            'county_district': self.county_district,
            'state': self.state,
            'total_area': self.total_area,
            'unit': self.unit,
            'ownership_type': self.ownership_type,
            'default_soil_type': self.default_soil_type,
            'water_source_primary': self.water_source_primary,
            'elevation_meters': self.elevation_meters,
            'slope_percentage': self.slope_percentage,
            'notes': self.notes,
            'field_count': self.fields.count(),
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Farm id={self.id} name='{self.name}'>"


class FarmDocument(db.Model):
    """Document/attachment associated with a farm property."""
    __tablename__ = 'farm_documents'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    doc_type = db.Column(db.String(50), default='Deed')  # Deed, Lease, Survey, Soil Map
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'title': self.title,
            'doc_type': self.doc_type,
            'file_path': self.file_path,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class FarmLocation(db.Model):
    """Geographic coordinate parameters for farm location."""
    __tablename__ = 'farm_locations'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    agro_climatic_zone = db.Column(db.String(100), default='Zone 4 - Temperate')
    micro_climate_notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'agro_climatic_zone': self.agro_climatic_zone,
            'micro_climate_notes': self.micro_climate_notes
        }


class FarmEquipment(db.Model):
    """Agricultural machinery and tools registered for a farm."""
    __tablename__ = 'farm_equipment'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), default='Tractor') # Tractor, Harvester, Seeder, Sprayer, Pump
    purchase_year = db.Column(db.Integer, default=2022)
    condition_status = db.Column(db.String(30), default='Operational')

    farm = db.relationship('Farm', backref=db.backref('equipment', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'equipment_type': self.equipment_type,
            'purchase_year': self.purchase_year,
            'condition_status': self.condition_status
        }


class FarmCertifications(db.Model):
    """Organic, GAP, and eco-certifications earned by a farm."""
    __tablename__ = 'farm_certifications'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    certification_name = db.Column(db.String(150), nullable=False)
    issuing_body = db.Column(db.String(150), nullable=False)
    valid_until = db.Column(db.Date, nullable=False)

    farm = db.relationship('Farm', backref=db.backref('certifications', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'certification_name': self.certification_name,
            'issuing_body': self.issuing_body,
            'valid_until': self.valid_until.strftime('%Y-%m-%d')
        }


class FarmResource(db.Model):
    """Inventory resources (fuel, seeds, compost) assigned to a farm."""
    __tablename__ = 'farm_resources'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    resource_name = db.Column(db.String(100), nullable=False)
    quantity_available = db.Column(db.Float, default=0.0)
    unit_of_measure = db.Column(db.String(20), default='Kg')

    farm = db.relationship('Farm', backref=db.backref('resources', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'resource_name': self.resource_name,
            'quantity_available': self.quantity_available,
            'unit_of_measure': self.unit_of_measure
        }

