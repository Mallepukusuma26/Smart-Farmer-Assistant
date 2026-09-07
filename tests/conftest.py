import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.farmer import Farmer
from app.models.crop import Crop
from app.models.farm import Farm
from app.models.field import Field

@pytest.fixture
def app():
    """Create test Flask app instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        
        # Seed test crop
        c = Crop(name='Test Rice', category='Cereal', season='Kharif', min_ph=5.5, max_ph=7.0, base_yield_per_acre=3.0)
        db.session.add(c)
        db.session.commit()
        
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for HTTP route testing."""
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def farmer_user(app):
    """Fixture for authenticated farmer user."""
    user = User(username='test_farmer', email='farmer@test.org', role='FARMER')
    user.set_password('pass123')
    db.session.add(user)
    db.session.flush()

    farmer = Farmer(user_id=user.id, full_name='Test Farmer', region='Zone A', total_land_area=5.0)
    db.session.add(farmer)
    db.session.commit()

    farm = Farm(farmer_id=farmer.id, name='Test Farm', location='Loc A', total_area=5.0)
    db.session.add(farm)
    db.session.flush()

    field = Field(farm_id=farm.id, field_name='Field 1', area=2.5)
    db.session.add(field)
    db.session.commit()

    return user

@pytest.fixture
def admin_user(app):
    """Fixture for authenticated admin user."""
    user = User(username='test_admin', email='admin@test.org', role='ADMIN')
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()
    return user
