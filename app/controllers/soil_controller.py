"""
Soil Controller Module for Smart Farmer Assistant.

Manages soil sample registration, pH/NPK laboratory analysis, organic carbon,
electrical conductivity, moisture records, soil quality scores, nutrient deficiency detection,
and automated soil improvement recommendations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.soil_service import SoilService
from app.services.field_service import FieldService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.soil_validator import SoilRecordValidator
from app.schemas.soil_schema import SoilSchema
import logging

logger = logging.getLogger(__name__)


class SoilController(BaseController):
    """
    Controller handling soil sample registration, physical/chemical parameter processing,
    deficiency detection algorithms, quality score evaluation, and amendment advice.
    """

    def __init__(self):
        self.soil_service = SoilService()
        self.field_service = FieldService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = SoilRecordValidator()
        self.soil_schema = SoilSchema()

    def list_samples(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists soil samples for the current farmer or field.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        field_id = request.args.get("field_id", type=int)
        if field_id:
            samples, total = self.soil_service.get_samples_by_field_paginated(field_id, page=page, per_page=per_page, filters=filters)
        else:
            farmer = self.farmer_service.get_farmer_by_user_id(user_id)
            if not farmer:
                samples, total = [], 0
            else:
                samples, total = self.soil_service.get_samples_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.soil_schema.dump_list(samples)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/soil_analysis.html",
            samples=samples,
            samples_data=serialized,
            field_id=field_id,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def analyze_soil(self) -> Union[str, Tuple[Response, int]]:
        """
        Registers new soil test data, runs physical/chemical classification algorithm,
        calculates health score, detects nutrient deficiencies, and stores soil record.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.soil_analysis"))

        try:
            sample = self.soil_service.create_and_analyze_soil_sample(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="SOIL_SAMPLE_ANALYZED",
                entity_type="SoilSample",
                entity_id=sample.id,
                details={
                    "field_id": sample.field_id,
                    "quality_score": sample.soil_quality_score,
                    "soil_type": sample.soil_type
                }
            )

            serialized = self.soil_schema.dump_single(sample)
            if request.is_json:
                return self.success_response(
                    data=serialized,
                    message="Soil sample analyzed successfully",
                    status_code=201
                )

            flash(f"Soil analysis complete! Health Score: {sample.soil_quality_score}/100 ({sample.soil_health_category})", "success")
            return redirect(url_for("farmer.get_sample_detail", sample_id=sample.id))

        except Exception as e:
            return self.handle_exception(e, "Error evaluating soil sample")

    def get_sample_detail(self, sample_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves complete soil analysis report including NPK charts, pH rating, recommendations.
        """
        sample = self.soil_service.get_sample_by_id(sample_id)
        if not sample:
            return self.error_response(message="Soil sample record not found", status_code=404)

        serialized = self.soil_schema.dump_single(sample)
        recommendations = self.soil_service.get_soil_amendment_recommendations(sample)

        context = {
            "sample": sample,
            "sample_data": serialized,
            "recommendations": recommendations
        }

        return self.render_or_json("farmer/soil_detail.html", context)

    def delete_sample(self, sample_id: int) -> Union[Response, str]:
        """
        Deletes a soil sample record.
        """
        user_id = self.get_current_user_id()
        sample = self.soil_service.get_sample_by_id(sample_id)
        if not sample:
            return self.error_response(message="Soil sample not found", status_code=404)

        try:
            self.soil_service.delete_sample(sample_id)
            self.audit_service.log_event(
                user_id=user_id,
                action="SOIL_SAMPLE_DELETED",
                entity_type="SoilSample",
                entity_id=sample_id
            )

            if request.is_json:
                return self.success_response(message="Soil sample record deleted successfully")

            flash("Soil sample record deleted.", "info")
            return redirect(url_for("farmer.list_samples"))

        except Exception as e:
            return self.handle_exception(e, "Error deleting soil sample")
