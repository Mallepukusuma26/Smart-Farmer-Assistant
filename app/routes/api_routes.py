from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services import SoilService, CropService, FinanceService
from ml.feature_engineering.feature_builder import compute_soil_health_score

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/soil-score', methods=['POST'])
def calculate_soil_score():
    data = request.json or {}
    ph = float(data.get('ph', 6.5))
    n = float(data.get('nitrogen', 100))
    p = float(data.get('phosphorus', 40))
    k = float(data.get('potassium', 120))
    oc = float(data.get('organic_carbon', 0.75))
    ec = float(data.get('electrical_conductivity', 0.5))

    score = compute_soil_health_score(ph, n, p, k, oc, ec)
    return jsonify({'health_score': score})


@api_bp.route('/crop-recommend', methods=['POST'])
def api_crop_recommend():
    data = request.json or {}
    n = float(data.get('n', 90))
    p = float(data.get('p', 40))
    k = float(data.get('k', 40))
    temp = float(data.get('temperature', 25))
    hum = float(data.get('humidity', 70))
    ph = float(data.get('ph', 6.5))
    rain = float(data.get('rainfall', 100))

    recs = CropService.recommend_crops(n, p, k, temp, hum, ph, rain)
    return jsonify({'recommendations': recs})


@api_bp.route('/financial-summary')
@login_required
def financial_summary_api():
    farmer = current_user.farmer_profile
    if not farmer:
        return jsonify({'error': 'Not a farmer'}), 400

    summary = FinanceService.get_financial_summary(farmer.id)
    return jsonify(summary)
