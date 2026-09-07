import pytest
from app.services import AuthService, SoilService, FertilizerService, FinanceService

def test_auth_service_register(app):
    user, msg = AuthService.register_user('service_user', 'service@test.org', 'password123', role='FARMER')
    assert user is not None
    assert user.username == 'service_user'
    assert user.farmer_profile is not None

def test_soil_service_analysis(app, farmer_user):
    from app.models.field import Field
    field = Field.query.first()
    record = SoilService.analyze_and_save_soil(field.id, ph=6.5, nitrogen=140, phosphorus=50, potassium=200)
    assert record is not None
    assert record.health_score > 70.0

def test_finance_service_expenses(app, farmer_user):
    farmer = farmer_user.farmer_profile
    exp = FinanceService.add_expense(farmer.id, 'Seeds', 250.0, 'Hybrid Seeds')
    assert exp.id is not None
    summary = FinanceService.get_financial_summary(farmer.id)
    assert summary['total_expense'] == 250.0
