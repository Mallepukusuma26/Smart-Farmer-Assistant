"""
Profit Controller Module for Smart Farmer Assistant.

Manages offline machine learning farm profitability forecasting, cost vs revenue projections,
break-even analysis, market price sensitivity modeling, and profit optimization recommendations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.profit_service import ProfitService
from app.services.crop_service import CropService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.profit_validator import ProfitPredictionValidator
from app.schemas.profit_schema import ProfitSchema
from ml.prediction.profit_predictor import ProfitPredictor
import logging

logger = logging.getLogger(__name__)


class ProfitController(BaseController):
    """
    Controller providing offline ML profitability forecasts, break-even price math,
    crop enterprise budget comparison, and profit maximization advice.
    """

    def __init__(self):
        self.profit_service = ProfitService()
        self.crop_service = CropService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = ProfitPredictionValidator()
        self.profit_schema = ProfitSchema()
        self.profit_predictor = ProfitPredictor()

    def predict_profit(self) -> Union[str, Tuple[Response, int]]:
        """
        Runs offline ML farm profitability model calculating projected revenue, total expenses,
        expected net profit, profit per acre, break-even market price, and ROI percentage.
        """
        if request.method == "GET":
            crops = self.crop_service.get_all_crops()
            return render_template("farmer/profit_prediction.html", crops=crops)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.predict_profit"))

        try:
            crop_name = data.get("crop_name", "rice").strip().lower()
            land_area_acres = float(data.get("land_area_acres", 5.0))
            seed_cost = float(data.get("seed_cost", 200.0))
            fertilizer_cost = float(data.get("fertilizer_cost", 400.0))
            pesticide_cost = float(data.get("pesticide_cost", 150.0))
            labour_cost = float(data.get("labour_cost", 500.0))
            irrigation_cost = float(data.get("irrigation_cost", 250.0))
            machinery_cost = float(data.get("machinery_cost", 300.0))
            other_cost = float(data.get("other_cost", 100.0))
            expected_yield_per_acre = float(data.get("expected_yield_per_acre", 3.5))
            expected_market_price = float(data.get("expected_market_price_per_tonne", 500.0))

            total_expenses_per_acre = seed_cost + fertilizer_cost + pesticide_cost + labour_cost + irrigation_cost + machinery_cost + other_cost
            total_investment = total_expenses_per_acre * land_area_acres
            expected_total_production = expected_yield_per_acre * land_area_acres
            expected_gross_revenue = expected_total_production * expected_market_price

            # Run ML model refinement
            predicted_profit = self.profit_predictor.predict_profit(
                crop_name=crop_name,
                total_investment=total_investment,
                land_area_acres=land_area_acres,
                expected_yield_per_acre=expected_yield_per_acre,
                market_price=expected_market_price
            )

            predicted_roi_pct = round((predicted_profit / total_investment) * 100, 2) if total_investment > 0 else 0.0
            break_even_price = round(total_expenses_per_acre / expected_yield_per_acre, 2) if expected_yield_per_acre > 0 else 0.0
            break_even_yield = round(total_expenses_per_acre / expected_market_price, 2) if expected_market_price > 0 else 0.0

            user_id = self.get_current_user_id()
            farmer = self.farmer_service.get_farmer_by_user_id(user_id) if user_id else None

            prediction_record = self.profit_service.create_profit_prediction(
                farmer_id=farmer.id if farmer else None,
                crop_name=crop_name,
                land_area_acres=land_area_acres,
                total_investment=total_investment,
                expected_gross_revenue=expected_gross_revenue,
                predicted_net_profit=predicted_profit,
                predicted_roi_pct=predicted_roi_pct,
                break_even_price=break_even_price,
                break_even_yield=break_even_yield,
                input_parameters=data
            )

            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="PROFIT_PREDICTION_GENERATED",
                    entity_type="ProfitPrediction",
                    entity_id=prediction_record.id,
                    details={"crop_name": crop_name, "predicted_net_profit": predicted_profit, "roi": predicted_roi_pct}
                )

            res_payload = {
                "record": self.profit_schema.dump_single(prediction_record),
                "crop_name": crop_name,
                "land_area_acres": land_area_acres,
                "total_investment": round(total_investment, 2),
                "expected_gross_revenue": round(expected_gross_revenue, 2),
                "predicted_net_profit": round(predicted_profit, 2),
                "predicted_profit_per_acre": round(predicted_profit / land_area_acres, 2),
                "predicted_roi_pct": predicted_roi_pct,
                "break_even_market_price_per_tonne": break_even_price,
                "break_even_yield_per_acre_tonnes": break_even_yield,
                "is_profitable": predicted_profit > 0
            }

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res_payload, message="Profitability prediction completed successfully")

            crops = self.crop_service.get_all_crops()
            return render_template(
                "farmer/profit_prediction.html",
                crops=crops,
                result=res_payload,
                form_data=data
            )

        except Exception as e:
            return self.handle_exception(e, "Error calculating profitability prediction")
