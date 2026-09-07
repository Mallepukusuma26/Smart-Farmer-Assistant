import pytest
from app.models.user import User
from app.models.farm import Farm
from app.models.soil import SoilRecord

def test_user_password_hashing(app):
    user = User(username='hash_test', email='hash@test.org', role='FARMER')
    user.set_password('Secret123')
    assert user.password_hash != 'Secret123'
    assert user.check_password('Secret123') is True
    assert user.check_password('WrongPass') is False

def test_user_roles(app):
    admin = User(role='ADMIN')
    farmer = User(role='FARMER')
    advisor = User(role='ADVISOR')

    assert admin.is_admin() is True
    assert farmer.is_farmer() is True
    assert advisor.is_advisor() is True

def test_soil_record_dict(app):
    record = SoilRecord(ph=6.5, nitrogen=140.0, health_score=85.0)
    d = record.to_dict()
    assert d['ph'] == 6.5
    assert d['nitrogen'] == 140.0
    assert d['health_score'] == 85.0
