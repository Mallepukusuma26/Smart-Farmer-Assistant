"""
REST API Routes Blueprint for Smart Farmer Assistant.

Exposes RESTful JSON endpoints for auth, farmers, farms, fields, soil, crops,
fertilizers, irrigation, disease, yield, finance, reports, notifications, search, and ML status.
"""

from flask import Blueprint, request
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.farmer_controller import FarmerController
from app.controllers.farm_controller import FarmController
from app.controllers.field_controller import FieldController
from app.controllers.soil_controller import SoilController
from app.controllers.crop_controller import CropController
from app.controllers.fertilizer_controller import FertilizerController
from app.controllers.irrigation_controller import IrrigationController
from app.controllers.disease_controller import DiseaseController
from app.controllers.yield_controller import YieldController
from app.controllers.finance_controller import FinanceController
from app.controllers.profit_controller import ProfitController
from app.controllers.advisor_controller import AdvisorController
from app.controllers.report_controller import ReportController
from app.controllers.notification_controller import NotificationController
from app.controllers.search_controller import SearchController
from app.controllers.ml_controller import MLController

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

auth_c = AuthController()
user_c = UserController()
farmer_c = FarmerController()
farm_c = FarmController()
field_c = FieldController()
soil_c = SoilController()
crop_c = CropController()
fert_c = FertilizerController()
irrig_c = IrrigationController()
disease_c = DiseaseController()
yield_c = YieldController()
finance_c = FinanceController()
profit_c = ProfitController()
advisor_c = AdvisorController()
report_c = ReportController()
notif_c = NotificationController()
search_c = SearchController()
ml_c = MLController()


# Auth API
@api_bp.route("/auth/register", methods=["POST"])
def api_register():
    return auth_c.register()


@api_bp.route("/auth/login", methods=["POST"])
def api_login():
    return auth_c.login()


@api_bp.route("/auth/logout", methods=["POST"])
def api_logout():
    return auth_c.logout()


@api_bp.route("/auth/profile", methods=["GET", "PUT"])
def api_profile():
    if request.method == "GET":
        return auth_c.profile()
    return auth_c.profile()


# Farmer & Farm API
@api_bp.route("/farmers", methods=["GET"])
def api_farmers():
    return farmer_c.list_farmers()


@api_bp.route("/farms", methods=["GET", "POST"])
def api_farms():
    if request.method == "GET":
        return farm_c.list_farms()
    return farm_c.create_farm()


@api_bp.route("/farms/<int:farm_id>", methods=["GET", "PUT", "DELETE"])
def api_farm_detail(farm_id):
    if request.method == "GET":
        return farm_c.get_farm_detail(farm_id)
    elif request.method == "PUT":
        return farm_c.update_farm(farm_id)
    return farm_c.delete_farm(farm_id)


# Field API
@api_bp.route("/fields", methods=["GET", "POST"])
def api_fields():
    if request.method == "GET":
        return field_c.list_fields()
    return field_c.create_field()


@api_bp.route("/fields/<int:field_id>", methods=["GET", "PUT", "DELETE"])
def api_field_detail(field_id):
    if request.method == "GET":
        return field_c.get_field_detail(field_id)
    elif request.method == "PUT":
        return field_c.update_field(field_id)
    return field_c.delete_field(field_id)


# Soil API
@api_bp.route("/soil", methods=["GET", "POST"])
def api_soil():
    if request.method == "GET":
        return soil_c.list_samples()
    return soil_c.analyze_soil()


# Crop API & ML Recommendation
@api_bp.route("/crops", methods=["GET", "POST"])
def api_crops():
    if request.method == "GET":
        return crop_c.list_crops()
    return crop_c.create_crop()


@api_bp.route("/ml/crop-recommendation", methods=["POST"])
def api_crop_recommendation():
    return crop_c.recommend_crops()


# Fertilizer API
@api_bp.route("/fertilizers", methods=["GET", "POST"])
def api_fertilizers():
    if request.method == "GET":
        return fert_c.list_fertilizers()
    return fert_c.create_fertilizer()


@api_bp.route("/ml/fertilizer-recommendation", methods=["POST"])
def api_fertilizer_recommendation():
    return fert_c.recommend_fertilizer()


# Irrigation API
@api_bp.route("/irrigation", methods=["GET", "POST"])
def api_irrigation():
    if request.method == "GET":
        return irrig_c.list_records()
    return irrig_c.calculate_schedule()


# Disease Vision API
@api_bp.route("/ml/disease-detection", methods=["POST"])
def api_disease_detection():
    return disease_c.detect_disease()


# Yield Regression API
@api_bp.route("/ml/yield-prediction", methods=["POST"])
def api_yield_prediction():
    return yield_c.predict_yield()


# Finance & Profit API
@api_bp.route("/finance/expenses", methods=["GET", "POST"])
def api_expenses():
    if request.method == "GET":
        return finance_c.list_expenses()
    return finance_c.add_expense()


@api_bp.route("/finance/revenue", methods=["GET", "POST"])
def api_revenue():
    if request.method == "GET":
        return finance_c.list_revenue()
    return finance_c.add_revenue()


@api_bp.route("/ml/profit-prediction", methods=["POST"])
def api_profit_prediction():
    return profit_c.predict_profit()


# Search & ML System Status
@api_bp.route("/search", methods=["GET"])
def api_search():
    return search_c.search()


@api_bp.route("/ml/status", methods=["GET"])
def api_ml_status():
    return ml_c.get_ml_status()
