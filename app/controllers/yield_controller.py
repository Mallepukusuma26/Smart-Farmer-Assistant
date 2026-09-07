"""
Yield Controller Module for Smart Farmer Assistant.

Manages offline crop yield forecasting using machine learning regression models
(Linear Regression, Random Forest Regressor, Gradient Boosting Regressor, Decision Tree Regressor),
historical yield logs, field acreage scaling, and expected revenue projections.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.yield_service import YieldService
from app.services.field_service import FieldService
from app.services.crop_service import CropService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.schemas.yield_schema import YieldSchema
from ml.prediction.yield_predictor import YieldPredictor
import logging

logger = logging.getLogger(__name__)


class YieldController(BaseController):
    """
    Controller providing ML yield estimation, expected metric tonnes per acre calculations,
    yield history logging, and yield vs historical benchmark comparisons.
    """

    def __init__(self):
        self.yield_service = YieldService()
        self.field_service = FieldService()
        self.crop_service = CropService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.yield_schema = YieldSchema()
        self.yield_predictor = YieldPredictor()

    def list_predictions(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists historical crop yield forecasts and actual harvest records.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            records, total = [], 0
        else:
            records, total = self.yield_service.get_records_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.yield_schema.dump_list(records)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/yield_prediction.html",
            records=records,
            records_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def predict_yield(self) -> Union[str, Tuple[Response, int]]:
        """
        Runs offline ML yield regression model given crop type, rainfall, temperature,
        pesticide use, NPK soil levels, and field acreage.
        """
        if request.method == "GET":
            crops = self.crop_service.get_all_crops()
            fields = []
            user_id = self.get_current_user_id()
            if user_id:
                farmer = self.farmer_service.get_farmer_by_user_id(user_id)
                if farmer:
                    fields = self.field_service.get_fields_by_farmer_id(farmer.id)
            return render_template("farmer/yield_prediction.html", crops=crops, fields=fields)

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            crop_name = data.get("crop_name", "rice").strip().lower()
            rainfall_mm = float(data.get("rainfall_mm", data.get("rainfall", 1000.0)))
            pesticides_tonnes = float(data.get("pesticides_tonnes", 0.5))
            avg_temp = float(data.get("avg_temp", data.get("temperature", 26.0)))
            area_acres = float(data.get("area_acres", 1.0))
            field_id = data.get("field_id", type=int) if data.get("field_id") else None

            # Offline ML regressor prediction
            yield_per_acre = self.yield_predictor.predict_yield(
                crop_name=crop_name,
                rainfall_mm=rainfall_mm,
                pesticides_tonnes=pesticides_tonnes,
                avg_temp=avg_temp
            )

            total_expected_yield_tonnes = round(yield_per_acre * area_acres, 2)
            estimated_market_price = self.yield_service.get_estimated_market_price(crop_name)
            estimated_revenue = round(total_expected_yield_tonnes * estimated_market_price, 2)

            user_id = self.get_current_user_id()
            farmer = self.farmer_service.get_farmer_by_user_id(user_id) if user_id else None
            farmer_id = farmer.id if farmer else None

            # Save prediction record to DB
            yield_record = self.yield_service.create_yield_record(
                farmer_id=farmer_id,
                field_id=field_id,
                crop_name=crop_name,
                predicted_yield_per_acre=yield_per_acre,
                total_expected_yield=total_expected_yield_tonnes,
                estimated_revenue=estimated_revenue,
                input_parameters=data
            )

            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="YIELD_PREDICTION_GENERATED",
                    entity_type="YieldRecord",
                    entity_id=yield_record.id,
                    details={"crop_name": crop_name, "total_expected_yield": total_expected_yield_tonnes}
                )

            res_payload = {
                "record": self.yield_schema.dump_single(yield_record),
                "yield_per_acre_tonnes": round(yield_per_acre, 2),
                "total_expected_yield_tonnes": total_expected_yield_tonnes,
                "estimated_market_price_per_tonne": estimated_market_price,
                "estimated_revenue": estimated_revenue,
                "input_parameters": data
            }

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res_payload, message="Yield prediction calculated successfully")

            crops = self.crop_service.get_all_crops()
            return render_template(
                "farmer/yield_prediction.html",
                crops=crops,
                result=res_payload,
                form_data=data
            )

        except Exception as e:
            return self.handle_exception(e, "Error calculating yield prediction")
