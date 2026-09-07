"""
Farm Controller Module for Smart Farmer Assistant.

Manages creation, editing, deletion, listing, location coordinates, total acreage,
soil type records, and farm summary reports.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.farm_service import FarmService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.farm_validator import FarmValidator
from app.schemas.farm_schema import FarmSchema
import logging

logger = logging.getLogger(__name__)


class FarmController(BaseController):
    """
    Controller handling farm entity CRUD operations, farm boundary locations,
    farmer association, and farm analytical metrics.
    """

    def __init__(self):
        self.farm_service = FarmService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = FarmValidator()
        self.farm_schema = FarmSchema()

    def list_farms(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists all farms owned by the currently authenticated farmer or all farms if admin.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        if self.is_admin():
            farms, total = self.farm_service.get_farms_paginated(page=page, per_page=per_page, filters=filters)
        else:
            farmer = self.farmer_service.get_farmer_by_user_id(user_id)
            if not farmer:
                farms, total = [], 0
            else:
                farms, total = self.farm_service.get_farmer_farms_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.farm_schema.dump_list(farms)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/farms.html",
            farms=farms,
            farms_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def create_farm(self) -> Union[str, Tuple[Response, int]]:
        """
        Creates a new farm record for the logged-in farmer.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            farmer = self.farmer_service.create_farmer_profile_for_user(user_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        data["farmer_id"] = farmer.id

        is_valid, validation_errors = self.validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return render_template("farmer/farms.html", errors=validation_errors), 400

        try:
            farm = self.farm_service.create_farm(farmer.id, data)
            self.audit_service.log_event(
                user_id=user_id,
                action="FARM_CREATED",
                entity_type="Farm",
                entity_id=farm.id,
                details={"name": farm.name, "area": farm.total_area_acres}
            )

            serialized = self.farm_schema.dump_single(farm)
            if request.is_json:
                return self.success_response(data=serialized, message="Farm created successfully", status_code=201)

            flash(f"Farm '{farm.name}' created successfully!", "success")
            return redirect(url_for("farmer.list_farms"))

        except Exception as e:
            return self.handle_exception(e, "Error creating farm")

    def get_farm_detail(self, farm_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves detailed information for a specific farm including fields, soil profile, and crop history.
        """
        user_id = self.get_current_user_id()
        farm = self.farm_service.get_farm_by_id(farm_id)
        if not farm:
            return self.error_response(message="Farm not found", status_code=404)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not (self.is_admin() or (farmer and farm.farmer_id == farmer.id)):
            return self.error_response(message="Access denied", status_code=403)

        serialized = self.farm_schema.dump_single(farm)
        return self.render_or_json("farmer/farm_detail.html", {"farm": farm, "farm_data": serialized})

    def update_farm(self, farm_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Updates farm details, location, acreage, or description.
        """
        user_id = self.get_current_user_id()
        farm = self.farm_service.get_farm_by_id(farm_id)
        if not farm:
            return self.error_response(message="Farm not found", status_code=404)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not (self.is_admin() or (farmer and farm.farmer_id == farmer.id)):
            return self.error_response(message="Access denied", status_code=403)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data, is_update=True)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.get_farm_detail", farm_id=farm_id))

        try:
            updated_farm = self.farm_service.update_farm(farm_id, data)
            self.audit_service.log_event(
                user_id=user_id,
                action="FARM_UPDATED",
                entity_type="Farm",
                entity_id=farm_id
            )

            serialized = self.farm_schema.dump_single(updated_farm)
            if request.is_json:
                return self.success_response(data=serialized, message="Farm updated successfully")

            flash(f"Farm '{updated_farm.name}' updated successfully", "success")
            return redirect(url_for("farmer.get_farm_detail", farm_id=farm_id))

        except Exception as e:
            return self.handle_exception(e, "Error updating farm")

    def delete_farm(self, farm_id: int) -> Union[Response, str]:
        """
        Deletes a farm record and its associated field records after validation.
        """
        user_id = self.get_current_user_id()
        farm = self.farm_service.get_farm_by_id(farm_id)
        if not farm:
            return self.error_response(message="Farm not found", status_code=404)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not (self.is_admin() or (farmer and farm.farmer_id == farmer.id)):
            return self.error_response(message="Access denied", status_code=403)

        try:
            self.farm_service.delete_farm(farm_id)
            self.audit_service.log_event(
                user_id=user_id,
                action="FARM_DELETED",
                entity_type="Farm",
                entity_id=farm_id
            )

            if request.is_json:
                return self.success_response(message="Farm deleted successfully")

            flash("Farm deleted successfully", "info")
            return redirect(url_for("farmer.list_farms"))

        except Exception as e:
            return self.handle_exception(e, "Error deleting farm")
