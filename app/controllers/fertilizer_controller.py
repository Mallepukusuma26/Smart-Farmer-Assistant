"""
Fertilizer Controller Module for Smart Farmer Assistant.

Manages fertilizer database catalog, NPK ratio compositions, soil nutrient deficiency calculations,
dosage per acre/hectare formulas, application schedule planning, and cost calculation.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.fertilizer_service import FertilizerService
from app.services.soil_service import SoilService
from app.services.crop_service import CropService
from app.services.field_service import FieldService
from app.services.audit_service import AuditService
from app.validators.fertilizer_validator import FertilizerValidator
from app.schemas.fertilizer_schema import FertilizerSchema
import logging

logger = logging.getLogger(__name__)


class FertilizerController(BaseController):
    """
    Controller providing fertilizer database management, deficiency calculations,
    application dose recommendations, stage scheduling, and cost tracking.
    """

    def __init__(self):
        self.fertilizer_service = FertilizerService()
        self.soil_service = SoilService()
        self.crop_service = CropService()
        self.field_service = FieldService()
        self.audit_service = AuditService()
        self.validator = FertilizerValidator()
        self.fertilizer_schema = FertilizerSchema()

    def list_fertilizers(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists available fertilizer master catalog items.
        """
        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        fertilizers, total = self.fertilizer_service.get_fertilizers_paginated(page=page, per_page=per_page, filters=filters)
        serialized = self.fertilizer_schema.dump_list(fertilizers)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "admin/fertilizers.html" if self.is_admin() else "farmer/fertilizer_recommendation.html",
            fertilizers=fertilizers,
            fertilizers_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def recommend_fertilizer(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates exact NPK deficiency for selected crop and soil sample,
        computes required dosage per acre, application split schedule, and total estimated cost.
        """
        if request.method == "GET":
            crops = self.crop_service.get_all_crops()
            field_id = request.args.get("field_id", type=int)
            soil_sample = None
            if field_id:
                soil_sample = self.soil_service.get_latest_sample_by_field(field_id)

            return render_template(
                "farmer/fertilizer_recommendation.html",
                crops=crops,
                soil_sample=soil_sample,
                field_id=field_id
            )

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            crop_id = data.get("crop_id")
            field_area = float(data.get("area_acres", 1.0))
            soil_n = float(data.get("soil_nitrogen", 50))
            soil_p = float(data.get("soil_phosphorus", 30))
            soil_k = float(data.get("soil_potassium", 40))

            crop = self.crop_service.get_crop_by_id(crop_id)
            if not crop:
                msg = "Selected crop not found"
                if request.is_json:
                    return self.error_response(message=msg, status_code=400)
                flash(msg, "danger")
                return redirect(url_for("farmer.recommend_fertilizer"))

            # Calculate fertilizer requirement and application schedule
            recommendation_result = self.fertilizer_service.calculate_fertilizer_recommendation(
                crop=crop,
                soil_n=soil_n,
                soil_p=soil_p,
                soil_k=soil_k,
                area_acres=field_area
            )

            user_id = self.get_current_user_id()
            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="FERTILIZER_RECOMMENDATION_CALCULATED",
                    entity_type="FertilizerRecommendation",
                    entity_id=0,
                    details={"crop_id": crop.id, "area": field_area}
                )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=recommendation_result, message="Fertilizer recommendation calculated successfully")

            crops = self.crop_service.get_all_crops()
            return render_template(
                "farmer/fertilizer_recommendation.html",
                crops=crops,
                result=recommendation_result,
                form_data=data
            )

        except Exception as e:
            return self.handle_exception(e, "Error calculating fertilizer recommendation")

    def create_fertilizer(self) -> Union[str, Tuple[Response, int]]:
        """
        Admin endpoint to add a new fertilizer to the system database.
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
            return redirect(url_for("admin.list_fertilizers"))

        try:
            fertilizer = self.fertilizer_service.create_fertilizer(data)
            self.audit_service.log_event(
                user_id=self.get_current_user_id(),
                action="FERTILIZER_CREATED",
                entity_type="Fertilizer",
                entity_id=fertilizer.id,
                details={"name": fertilizer.name}
            )

            serialized = self.fertilizer_schema.dump_single(fertilizer)
            if request.is_json:
                return self.success_response(data=serialized, message="Fertilizer created successfully", status_code=201)

            flash(f"Fertilizer '{fertilizer.name}' added successfully", "success")
            return redirect(url_for("admin.list_fertilizers"))

        except Exception as e:
            return self.handle_exception(e, "Error creating fertilizer")
