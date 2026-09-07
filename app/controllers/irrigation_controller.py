"""
Irrigation Controller Module for Smart Farmer Assistant.

Manages field irrigation logs, water source records, ET-based crop water requirement
calculations, soil moisture balance, irrigation frequency/duration recommendations,
water consumption tracking, and estimated pumping cost calculation.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.irrigation_service import IrrigationService
from app.services.field_service import FieldService
from app.services.crop_service import CropService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.irrigation_validator import IrrigationScheduleValidator
from app.schemas.irrigation_schema import IrrigationSchema
import logging

logger = logging.getLogger(__name__)


class IrrigationController(BaseController):
    """
    Controller handling field water requirements, ET-based evapotranspiration math,
    irrigation log records, soil moisture deficit alerts, and water expense tracking.
    """

    def __init__(self):
        self.irrigation_service = IrrigationService()
        self.field_service = FieldService()
        self.crop_service = CropService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = IrrigationScheduleValidator()
        self.irrigation_schema = IrrigationSchema()

    def list_records(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists historical irrigation records for the farmer or specific field.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        field_id = request.args.get("field_id", type=int)
        if field_id:
            records, total = self.irrigation_service.get_records_by_field_paginated(field_id, page=page, per_page=per_page, filters=filters)
        else:
            farmer = self.farmer_service.get_farmer_by_user_id(user_id)
            if not farmer:
                records, total = [], 0
            else:
                records, total = self.irrigation_service.get_records_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.irrigation_schema.dump_list(records)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/irrigation_schedule.html",
            records=records,
            records_data=serialized,
            field_id=field_id,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def calculate_schedule(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates field-specific irrigation requirement using local ET evapotranspiration model,
        soil moisture deficit, crop stage factor (Kc), and field area.
        """
        if request.method == "GET":
            field_id = request.args.get("field_id", type=int)
            field = self.field_service.get_field_by_id(field_id) if field_id else None
            return render_template("farmer/irrigation_schedule.html", field=field, field_id=field_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            field_id = data.get("field_id")
            field = self.field_service.get_field_by_id(field_id)
            crop_stage = data.get("growth_stage", "mid")
            temp_c = float(data.get("temperature", 28.0))
            humidity = float(data.get("humidity", 60.0))
            soil_moisture_pct = float(data.get("soil_moisture_pct", 35.0))

            if not field:
                msg = "Field record not found"
                if request.is_json:
                    return self.error_response(message=msg, status_code=404)
                flash(msg, "danger")
                return redirect(url_for("farmer.list_records"))

            schedule_result = self.irrigation_service.calculate_field_irrigation_requirement(
                field=field,
                growth_stage=crop_stage,
                temperature=temp_c,
                humidity=humidity,
                current_soil_moisture=soil_moisture_pct
            )

            user_id = self.get_current_user_id()
            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="IRRIGATION_SCHEDULE_CALCULATED",
                    entity_type="IrrigationRecord",
                    entity_id=0,
                    details={"field_id": field.id, "recommended_liters": schedule_result.get("recommended_liters")}
                )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=schedule_result, message="Irrigation schedule calculated successfully")

            return render_template(
                "farmer/irrigation_schedule.html",
                field=field,
                result=schedule_result,
                form_data=data
            )

        except Exception as e:
            return self.handle_exception(e, "Error calculating irrigation requirement")

    def log_irrigation(self) -> Union[str, Tuple[Response, int]]:
        """
        Logs a completed irrigation event for water usage and expense tracking.
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
            return redirect(url_for("farmer.list_records"))

        try:
            record = self.irrigation_service.log_irrigation_event(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="IRRIGATION_LOGGED",
                entity_type="IrrigationRecord",
                entity_id=record.id,
                details={"field_id": record.field_id, "water_amount_liters": record.water_amount_liters}
            )

            serialized = self.irrigation_schema.dump_single(record)
            if request.is_json:
                return self.success_response(data=serialized, message="Irrigation log saved successfully", status_code=201)

            flash("Irrigation log recorded successfully!", "success")
            return redirect(url_for("farmer.list_records"))

        except Exception as e:
            return self.handle_exception(e, "Error logging irrigation event")
