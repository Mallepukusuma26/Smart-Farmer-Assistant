"""
Farmer Routes Blueprint for Smart Farmer Assistant.

Maps routes for the main Farmer Dashboard, farmer profiles, farms, fields, soil analysis,
crop recommendations, fertilizer recommendations, irrigation, disease detection, yield prediction,
financial ledger, profitability, reports, and notifications.
"""

from flask import Blueprint, request
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
from app.controllers.report_controller import ReportController
from app.controllers.notification_controller import NotificationController
from app.controllers.search_controller import SearchController

farmer_bp = Blueprint("farmer", __name__, url_prefix="/farmer")

farmer_controller = FarmerController()
farm_controller = FarmController()
field_controller = FieldController()
soil_controller = SoilController()
crop_controller = CropController()
fertilizer_controller = FertilizerController()
irrigation_controller = IrrigationController()
disease_controller = DiseaseController()
yield_controller = YieldController()
finance_controller = FinanceController()
profit_controller = ProfitController()
report_controller = ReportController()
notification_controller = NotificationController()
search_controller = SearchController()


@farmer_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return farmer_controller.dashboard()


@farmer_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return farmer_controller.get_profile()
    return farmer_controller.update_profile()


# Farm Management Routes
@farmer_bp.route("/farms", methods=["GET", "POST"])
def list_farms():
    if request.method == "GET":
        return farm_controller.list_farms()
    return farm_controller.create_farm()


@farmer_bp.route("/farms/<int:farm_id>", methods=["GET", "POST", "PUT"])
def farm_detail(farm_id):
    if request.method == "GET":
        return farm_controller.get_farm_detail(farm_id)
    return farm_controller.update_farm(farm_id)


@farmer_bp.route("/farms/<int:farm_id>/delete", methods=["POST", "DELETE"])
def delete_farm(farm_id):
    return farm_controller.delete_farm(farm_id)


# Field Management Routes
@farmer_bp.route("/fields", methods=["GET", "POST"])
def list_fields():
    if request.method == "GET":
        return field_controller.list_fields()
    return field_controller.create_field()


@farmer_bp.route("/fields/<int:field_id>", methods=["GET", "POST", "PUT"])
def field_detail(field_id):
    if request.method == "GET":
        return field_controller.get_field_detail(field_id)
    return field_controller.update_field(field_id)


@farmer_bp.route("/fields/<int:field_id>/delete", methods=["POST", "DELETE"])
def delete_field(field_id):
    return field_controller.delete_field(field_id)


# Soil Analysis Routes
@farmer_bp.route("/soil-analysis", methods=["GET", "POST"])
def soil_analysis():
    if request.method == "GET":
        return soil_controller.list_samples()
    return soil_controller.analyze_soil()


@farmer_bp.route("/soil-analysis/<int:sample_id>", methods=["GET"])
def get_sample_detail(sample_id):
    return soil_controller.get_sample_detail(sample_id)


# Crop Recommendation & Management Routes
@farmer_bp.route("/crop-recommendation", methods=["GET", "POST"])
def crop_recommendation():
    return crop_controller.recommend_crops()


@farmer_bp.route("/crop-management", methods=["GET"])
def crop_management():
    return crop_controller.list_crops()


# Fertilizer Recommendation & Schedule Routes
@farmer_bp.route("/fertilizer-recommendation", methods=["GET", "POST"])
def fertilizer_recommendation():
    return fertilizer_controller.recommend_fertilizer()


# Irrigation Schedule Routes
@farmer_bp.route("/irrigation-schedule", methods=["GET", "POST"])
def irrigation_schedule():
    if request.method == "GET":
        return irrigation_controller.list_records()
    return irrigation_controller.calculate_schedule()


@farmer_bp.route("/irrigation-log", methods=["POST"])
def log_irrigation():
    return irrigation_controller.log_irrigation()


# Disease Detection Routes
@farmer_bp.route("/disease-detection", methods=["GET", "POST"])
def disease_detection():
    return disease_controller.detect_disease()


@farmer_bp.route("/disease-history", methods=["GET"])
def disease_history():
    return disease_controller.list_history()


@farmer_bp.route("/disease-detail/<int:record_id>", methods=["GET"])
def disease_detail(record_id):
    return disease_controller.get_diagnosis_detail(record_id)


# Yield Prediction Routes
@farmer_bp.route("/yield-prediction", methods=["GET", "POST"])
def yield_prediction():
    return yield_controller.predict_yield()


# Finance & Ledger Routes
@farmer_bp.route("/expenses", methods=["GET", "POST"])
def list_expenses():
    if request.method == "GET":
        return finance_controller.list_expenses()
    return finance_controller.add_expense()


@farmer_bp.route("/revenue", methods=["GET", "POST"])
def list_revenue():
    if request.method == "GET":
        return finance_controller.list_revenue()
    return finance_controller.add_revenue()


@farmer_bp.route("/profit-prediction", methods=["GET", "POST"])
def profit_prediction():
    return profit_controller.predict_profit()


# Reports & Export Routes
@farmer_bp.route("/reports", methods=["GET"])
def list_reports():
    return report_controller.list_reports()


@farmer_bp.route("/reports/generate", methods=["GET", "POST"])
def generate_report():
    return report_controller.generate_report()


# Notifications Routes
@farmer_bp.route("/notifications", methods=["GET"])
def list_notifications():
    return notification_controller.list_notifications()


@farmer_bp.route("/notifications/<int:notification_id>/read", methods=["POST"])
def mark_notification_read(notification_id):
    return notification_controller.mark_as_read(notification_id)


@farmer_bp.route("/notifications/mark-all-read", methods=["POST"])
def mark_all_notifications_read():
    return notification_controller.mark_all_as_read()


# Search Route
@farmer_bp.route("/search", methods=["GET"])
def search():
    return search_controller.search()
