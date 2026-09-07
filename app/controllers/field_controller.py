"""
Field Controller Module for Smart Farmer Assistant.

Manages creation, editing, deletion, field boundary data, field size, soil records,
crop assignments, irrigation assignments, and field health analytics.
"""

from typing import Dict, Any, Tuple, Union, Optional
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.field_service import FieldService
from app.services.farm_service import FarmService
from app.services.farmer_service import FarmerService
from app.services.crop_service import CropService
from app.services.soil_service import SoilService
from app.services.audit_service import AuditService
from app.validators.field_validator import FieldValidator
from app.schemas.field_schema import FieldSchema
import logging

logger = logging.getLogger(__name__)


class FieldController(BaseController):
    """
    Controller responsible for managing field plots within farms, field boundaries,
    soil specifications, crop assignments, disease history, and field analytics.
    """

    def __init__(self):
        self.field_service = FieldService()
        self.farm_service = FarmService()
        self.farmer_service = FarmerService()
        self.crop_service = CropService()
        self.soil_service = SoilService()
        self.audit_service = AuditService()
        self.validator = FieldValidator()
        self.field_schema = FieldSchema()

    def list_fields(self, farm_id: Optional[int] = None) -> Union[str, Tuple[Response, int]]:
        """
        Lists fields for a specific farm or across all user farms.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        if farm_id:
            fields, total = self.field_service.get_fields_by_farm_paginated(farm_id, page=page, per_page=per_page, filters=filters)
        else:
            farmer = self.farmer_service.get_farmer_by_user_id(user_id)
            if not farmer:
                fields, total = [], 0
            else:
                fields, total = self.field_service.get_fields_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.field_schema.dump_list(fields)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/fields.html",
            fields=fields,
            fields_data=serialized,
            farm_id=farm_id,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def create_field(self) -> Union[str, Tuple[Response, int]]:
        """
        Creates a new field plot inside a designated farm.
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
            return redirect(url_for("farmer.list_farms"))

        farm_id = data.get("farm_id")
        farm = self.farm_service.get_farm_by_id(farm_id)
        if not farm:
            return self.error_response(message="Target farm not found", status_code=404)

        try:
            field = self.field_service.create_field(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="FIELD_CREATED",
                entity_type="Field",
                entity_id=field.id,
                details={"name": field.name, "farm_id": farm.id, "area": field.area_acres}
            )

            serialized = self.field_schema.dump_single(field)
            if request.is_json:
                return self.success_response(data=serialized, message="Field created successfully", status_code=201)

            flash(f"Field '{field.name}' created successfully!", "success")
            return redirect(url_for("farmer.get_farm_detail", farm_id=farm_id))

        except Exception as e:
            return self.handle_exception(e, "Error creating field")

    def get_field_detail(self, field_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves detailed field plot metrics, soil record history, crop assignment, and irrigation records.
        """
        user_id = self.get_current_user_id()
        field = self.field_service.get_field_by_id(field_id)
        if not field:
            return self.error_response(message="Field not found", status_code=404)

        serialized = self.field_schema.dump_single(field)
        soil_samples = self.soil_service.get_samples_by_field_id(field_id)
        current_crop = self.crop_service.get_crop_by_id(field.current_crop_id) if field.current_crop_id else None

        context = {
            "field": field,
            "field_data": serialized,
            "soil_samples": soil_samples,
            "current_crop": current_crop
        }

        return self.render_or_json("farmer/field_detail.html", context)

    def update_field(self, field_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Updates field boundary, area, crop assignment, or soil type.
        """
        user_id = self.get_current_user_id()
        field = self.field_service.get_field_by_id(field_id)
        if not field:
            return self.error_response(message="Field not found", status_code=404)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.validator.validate(data, is_update=True)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.get_field_detail", field_id=field_id))

        try:
            updated_field = self.field_service.update_field(field_id, data)
            self.audit_service.log_event(
                user_id=user_id,
                action="FIELD_UPDATED",
                entity_type="Field",
                entity_id=field_id
            )

            serialized = self.field_schema.dump_single(updated_field)
            if request.is_json:
                return self.success_response(data=serialized, message="Field updated successfully")

            flash(f"Field '{updated_field.name}' updated successfully", "success")
            return redirect(url_for("farmer.get_field_detail", field_id=field_id))

        except Exception as e:
            return self.handle_exception(e, "Error updating field")

    def delete_field(self, field_id: int) -> Union[Response, str]:
        """
        Deletes a field plot record.
        """
        user_id = self.get_current_user_id()
        field = self.field_service.get_field_by_id(field_id)
        if not field:
            return self.error_response(message="Field not found", status_code=404)

        farm_id = field.farm_id
        try:
            self.field_service.delete_field(field_id)
            self.audit_service.log_event(
                user_id=user_id,
                action="FIELD_DELETED",
                entity_type="Field",
                entity_id=field_id
            )

            if request.is_json:
                return self.success_response(message="Field deleted successfully")

            flash("Field deleted successfully", "info")
            return redirect(url_for("farmer.get_farm_detail", farm_id=farm_id))

        except Exception as e:
            return self.handle_exception(e, "Error deleting field")
