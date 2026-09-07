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

def test_soil_intelligence_service():
    from app.services.soil_intelligence_service import SoilIntelligenceService
    service = SoilIntelligenceService()
    res = service.evaluate_nutrient_balance(150.0, 60.0, 200.0)
    assert res['is_balanced'] is True
    plan = service.generate_amendment_plan(5.5, 0.5, 2.5)
    assert len(plan['recommended_amendments']) >= 2

def test_fertilizer_intelligence_service():
    from app.services.fertilizer_intelligence_service import FertilizerIntelligenceService
    service = FertilizerIntelligenceService()
    res = service.calculate_npk_deficit_and_dosage(100.0, 30.0, 150.0, 'Wheat', 2.0)
    assert 'commercial_fertilizer_schedule' in res
    assert res['total_fertilizer_cost_inr'] > 0

def test_irrigation_intelligence_service():
    from app.services.irrigation_intelligence_service import IrrigationIntelligenceService
    service = IrrigationIntelligenceService()
    et0 = service.calculate_reference_et0(28.0, 60.0)
    assert et0 > 0.0
    cwr = service.calculate_crop_water_requirement('Wheat', 'Mid Season', et0, 1.0)
    assert cwr['daily_water_demand_liters'] > 0

def test_offline_disease_service():
    from app.services.offline_disease_service import OfflineDiseaseService
    service = OfflineDiseaseService()
    res = service.analyze_leaf_image_features()
    assert 'predicted_disease' in res
    assert res['model_confidence_pct'] > 50.0

def test_yield_prediction_service():
    from app.services.yield_prediction_service import YieldPredictionService
    service = YieldPredictionService()
    res = service.forecast_field_yield('Wheat', 2.0, 150.0, 60.0, 200.0, 650.0, 25.0)
    assert res['total_predicted_yield_tons'] > 0.0
