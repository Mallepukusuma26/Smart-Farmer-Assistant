"""
Farmer Controller Module for Smart Farmer Assistant.

Handles farmer profiles, farmer preference configuration, multi-farm administration,
location coordinates, documents, field counts, and farmer dashboard metrics.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.farmer_service import FarmerService
from app.services.farm_service import FarmService
from app.services.field_service import FieldService
from app.services.soil_service import SoilService
from app.services.crop_service import CropService
from app.services.audit_service import AuditService
from app.validators.farmer_validator import FarmerProfileValidator
from app.schemas.farmer_schema import FarmerSchema
from app.schemas.farm_schema import FarmSchema
import logging

logger = logging.getLogger(__name__)


class FarmerController(BaseController):
    """
    Controller responsible for managing Farmer entities, Farmer profile details,
    farm ownership, field assignments, activity logs, and farmer workspace views.
    """

    def __init__(self):
        self.farmer_service = FarmerService()
        self.farm_service = FarmService()
        self.field_service = FieldService()
        self.soil_service = SoilService()
        self.crop_service = CropService()
        self.audit_service = AuditService()
        self.validator = FarmerProfileValidator()
        self.farmer_schema = FarmerSchema()
        self.farm_schema = FarmSchema()

    def dashboard(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders the comprehensive Farmer Dashboard overview including farm stats,
        active fields, soil test summaries, recent recommendations, and notification widgets.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            farmer = self.farmer_service.create_farmer_profile_for_user(user_id)

        farms = self.farm_service.get_farms_by_farmer_id(farmer.id)
        total_farms = len(farms)
        total_fields = sum(len(farm.fields) for farm in farms)
        total_area = sum(float(farm.total_area_acres or 0) for farm in farms)

        recent_soil_samples = self.soil_service.get_recent_samples_by_farmer(farmer.id, limit=5)
        crop_summary = self.crop_service.get_farmer_crop_summary(farmer.id)

        dashboard_data = {
            "farmer": self.farmer_schema.dump_single(farmer),
            "total_farms": total_farms,
            "total_fields": total_fields,
            "total_area_acres": round(total_area, 2),
            "recent_soil_samples": recent_soil_samples,
            "crop_summary": crop_summary,
            "farms_list": [self.farm_schema.dump_single(f) for f in farms[:5]]
        }

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=dashboard_data)

        return render_template("farmer/dashboard.html", **dashboard_data)

    def get_profile(self) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves farmer profile and preferences settings.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            return self.error_response(message="Farmer profile not found", status_code=404)

        data = self.farmer_schema.dump_single(farmer)
        return self.render_or_json("farmer/profile.html", {"farmer": farmer, "farmer_data": data})

    def update_profile(self) -> Union[str, Tuple[Response, int]]:
        """
        Updates farmer details, agricultural experience, farming type, address, and preferences.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            return self.error_response(message="Farmer profile not found", status_code=404)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return render_template("farmer/profile.html", farmer=farmer, errors=validation_errors), 400

        try:
            updated_farmer = self.farmer_service.update_farmer(farmer.id, data)
            self.audit_service.log_event(
                user_id=user_id,
                action="FARMER_PROFILE_UPDATED",
                entity_type="Farmer",
                entity_id=farmer.id
            )

            if request.is_json:
                return self.success_response(
                    data=self.farmer_schema.dump_single(updated_farmer),
                    message="Farmer profile updated successfully"
                )

            flash("Profile updated successfully", "success")
            return redirect(url_for("farmer.profile"))

        except Exception as e:
            return self.handle_exception(e, "Error updating farmer profile")

    def list_farmers(self) -> Union[str, Tuple[Response, int]]:
        """
        Admin/Advisor view for listing, searching, and filtering all registered farmers.
        """
        if not (self.is_admin() or self.is_advisor()):
            return self.error_response(message="Access denied", status_code=403)

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        farmers, total = self.farmer_service.get_farmers_paginated(page=page, per_page=per_page, filters=filters)
        serialized = self.farmer_schema.dump_list(farmers)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "admin/farmers.html",
            farmers=farmers,
            farmers_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def get_farmer_detail(self, farmer_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves detailed farmer information including farms, fields, soil samples, and advice logs.
        """
        user_id = self.get_current_user_id()
        farmer = self.farmer_service.get_farmer_by_id(farmer_id)
        if not farmer:
            return self.error_response(message="Farmer not found", status_code=404)

        if not (self.is_admin() or self.is_advisor() or (farmer.user_id == user_id)):
            return self.error_response(message="Access denied", status_code=403)

        farms = self.farm_service.get_farms_by_farmer_id(farmer_id)
        farmer_data = self.farmer_schema.dump_single(farmer)
        farms_data = self.farm_schema.dump_list(farms)

        context = {
            "farmer": farmer,
            "farmer_data": farmer_data,
            "farms": farms,
            "farms_data": farms_data
        }

        return self.render_or_json("advisor/farmer_view.html", context)
