"""
Crop Controller Module for Smart Farmer Assistant.

Manages crop master repository, varieties, growth duration, temperature/rainfall/soil requirements,
pH ranges, NPK requirement calculations, crop rotation rules, and ML crop recommendation inference.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.crop_service import CropService
from app.services.soil_service import SoilService
from app.services.field_service import FieldService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.crop_validator import CropValidator
from app.schemas.crop_schema import CropSchema
from ml.prediction.crop_predictor import CropPredictor
import logging

logger = logging.getLogger(__name__)


class CropController(BaseController):
    """
    Controller managing crop catalog, agronomic growth conditions, crop suitability scoring,
    crop rotation rules, and ML offline crop recommendation service.
    """

    def __init__(self):
        self.crop_service = CropService()
        self.soil_service = SoilService()
        self.field_service = FieldService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = CropValidator()
        self.crop_schema = CropSchema()
        self.crop_predictor = CropPredictor()

    def list_crops(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists available crops with filtering by category, season, or soil type.
        """
        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        crops, total = self.crop_service.get_crops_paginated(page=page, per_page=per_page, filters=filters)
        serialized = self.crop_schema.dump_list(crops)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "admin/crops.html" if self.is_admin() else "farmer/crop_management.html",
            crops=crops,
            crops_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def recommend_crops(self) -> Union[str, Tuple[Response, int]]:
        """
        Processes offline ML crop recommendation request based on NPK, pH, temperature,
        humidity, and rainfall parameters.
        """
        if request.method == "GET":
            field_id = request.args.get("field_id", type=int)
            soil_sample = None
            if field_id:
                soil_sample = self.soil_service.get_latest_sample_by_field(field_id)

            return render_template("farmer/crop_recommendation.html", soil_sample=soil_sample, field_id=field_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            N = float(data.get("nitrogen", data.get("N", 50)))
            P = float(data.get("phosphorus", data.get("P", 50)))
            K = float(data.get("potassium", data.get("K", 50)))
            temperature = float(data.get("temperature", 25.0))
            humidity = float(data.get("humidity", 65.0))
            ph = float(data.get("ph", 6.5))
            rainfall = float(data.get("rainfall", 100.0))

            # Run offline ML prediction pipeline
            top_crops = self.crop_predictor.predict_top_n(
                N=N, P=P, K=K, temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall, top_n=5
            )

            # Retrieve database crop details for top recommendations
            recommendations = []
            for item in top_crops:
                crop_name = item["crop_name"]
                db_crop = self.crop_service.get_crop_by_name(crop_name)
                recommendations.append({
                    "crop_name": crop_name,
                    "confidence_score": round(item["confidence"] * 100, 2),
                    "db_crop": self.crop_schema.dump_single(db_crop) if db_crop else None,
                    "reasoning": f"Optimal fit for N:{N}, P:{P}, K:{K}, pH:{ph}"
                })

            user_id = self.get_current_user_id()
            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="CROP_RECOMMENDATION_GENERATED",
                    entity_type="CropRecommendation",
                    entity_id=0,
                    details={"input": data, "top_recommendation": top_crops[0]["crop_name"] if top_crops else None}
                )

            res_payload = {
                "recommendations": recommendations,
                "input_parameters": {"N": N, "P": P, "K": K, "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rainfall}
            }

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res_payload, message="Crop recommendations generated successfully")

            return render_template(
                "farmer/crop_recommendation.html",
                results=res_payload,
                recommendations=recommendations,
                form_data=data
            )

        except Exception as e:
            return self.handle_exception(e, "Error generating crop recommendations")

    def create_crop(self) -> Union[str, Tuple[Response, int]]:
        """
        Admin endpoint for adding a new crop to the master database.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("admin.list_crops"))

        try:
            crop = self.crop_service.create_crop(data)
            self.audit_service.log_event(
                user_id=self.get_current_user_id(),
                action="CROP_CREATED",
                entity_type="Crop",
                entity_id=crop.id,
                details={"name": crop.name}
            )

            serialized = self.crop_schema.dump_single(crop)
            if request.is_json:
                return self.success_response(data=serialized, message="Crop created successfully", status_code=201)

            flash(f"Crop '{crop.name}' added successfully", "success")
            return redirect(url_for("admin.list_crops"))

        except Exception as e:
            return self.handle_exception(e, "Error adding crop")

    def get_crop_detail(self, crop_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves detailed agronomic requirements for a specific crop.
        """
        crop = self.crop_service.get_crop_by_id(crop_id)
        if not crop:
            return self.error_response(message="Crop not found", status_code=404)

        serialized = self.crop_schema.dump_single(crop)
        return self.render_or_json("farmer/crop_detail.html", {"crop": crop, "crop_data": serialized})
