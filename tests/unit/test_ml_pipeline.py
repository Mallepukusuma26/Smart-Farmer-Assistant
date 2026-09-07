import pytest
import math
from ml.prediction.crop_predictor import CropPredictor
from ml.prediction.yield_predictor import YieldPredictor
from ml.prediction.profit_predictor import ProfitPredictor

def test_crop_predictor():
    predictor = CropPredictor()
    recs = predictor.predict(n=90, p=40, k=40, temperature=25.0, humidity=80.0, ph=6.5, rainfall=200.0)
    assert len(recs) == 3
    assert 'crop_name' in recs[0]
    assert recs[0]['suitability_score'] > 0
    assert 'prediction_source' in recs[0]

def test_crop_predictor_top_n_and_sanitization():
    predictor = CropPredictor()
    top_items = predictor.predict_top_n(n=-10, p=float('nan'), k=40, temperature=25.0, humidity=80.0, ph=6.5, rainfall=200.0, top_n=2)
    assert len(top_items) == 2
    assert 'crop_name' in top_items[0]
    assert 'confidence' in top_items[0]

def test_yield_predictor():
    predictor = YieldPredictor()
    res = predictor.predict(
        crop='Rice',
        soil_type='Loamy',
        area_acres=2.5,
        nitrogen=100,
        phosphorus=40,
        potassium=120,
        ph=6.5,
        temperature=28.0,
        rainfall=800.0,
        irrigation_liters=50000.0,
        fertilizer_kg=100.0
    )
    assert 'predicted_yield_tons' in res
    assert res['predicted_yield_tons'] > 0
    assert res['expected_range_min'] < res['expected_range_max']
    assert 'prediction_source' in res
    assert 'confidence_score' in res

def test_yield_predictor_predict_yield_helper_and_sanitization():
    predictor = YieldPredictor()
    y_per_acre = predictor.predict_yield(crop_name='rice', rainfall_mm=-500.0, pesticides_tonnes=float('nan'), avg_temp=28.0)
    assert y_per_acre > 0

def test_profit_predictor():
    predictor = ProfitPredictor()
    res = predictor.predict(crop='Rice', area_acres=2.5, yield_tons=10.0, selling_price_per_ton=350.0, estimated_expenses=1200.0)
    assert res['expected_revenue'] == 3500.0
    assert res['expected_profit'] > 0
    assert res['profit_margin_percent'] > 0

