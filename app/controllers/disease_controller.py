"""
Disease Controller Module for Smart Farmer Assistant.

Manages offline plant disease diagnosis using uploaded leaf images, computer vision feature extraction
(color histograms, texture GLCM, edge density, shape moments), local machine learning classifier inference,
confidence score estimation, disease severity ranking, and organic/chemical treatment advice.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.disease_service import DiseaseService
from app.services.field_service import FieldService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.validators.disease_validator import DiseaseImageUploadValidator
from app.schemas.disease_schema import DiseaseSchema
from ml.prediction.disease_predictor import DiseasePredictor
import os
import logging
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


class DiseaseController(BaseController):
    """
    Controller handling leaf image uploads, computer vision feature extraction,
    local ML classifier evaluation, disease diagnostic reports, and remedial treatments.
    """

    def __init__(self):
        self.disease_service = DiseaseService()
        self.field_service = FieldService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.validator = DiseaseImageUploadValidator()
        self.disease_schema = DiseaseSchema()
        self.disease_predictor = DiseasePredictor()

    def list_history(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists historical disease diagnosis scans performed by the farmer.
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
            records, total = self.disease_service.get_records_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.disease_schema.dump_list(records)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/disease_detection.html",
            records=records,
            records_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def detect_disease(self) -> Union[str, Tuple[Response, int]]:
        """
        Handles uploaded leaf image file, validates image format/dimensions,
        extracts color/texture/edge features, runs offline local ML model,
        estimates severity, and saves diagnostic disease record.
        """
        if request.method == "GET":
            fields = []
            user_id = self.get_current_user_id()
            if user_id:
                farmer = self.farmer_service.get_farmer_by_user_id(user_id)
                if farmer:
                    fields = self.field_service.get_fields_by_farmer_id(farmer.id)
            return render_template("farmer/disease_detection.html", fields=fields)

        # File check
        if "image" not in request.files and "file" not in request.files:
            msg = "No image file provided"
            if request.is_json:
                return self.error_response(message=msg, status_code=400)
            flash(msg, "danger")
            return redirect(url_for("farmer.disease_detection"))

        image_file = request.files.get("image") or request.files.get("file")
        if not image_file or image_file.filename == "":
            msg = "Please select a valid image file"
            if request.is_json:
                return self.error_response(message=msg, status_code=400)
            flash(msg, "danger")
            return redirect(url_for("farmer.disease_detection"))

        is_valid, validation_errors = self.validator.validate_file(image_file)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Invalid image upload", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.disease_detection"))

        try:
            # Save uploaded image locally
            user_id = self.get_current_user_id()
            farmer = self.farmer_service.get_farmer_by_user_id(user_id) if user_id else None
            farmer_id = farmer.id if farmer else None
            field_id = request.form.get("field_id", type=int)

            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join(os.getcwd(), "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            saved_path = os.path.join(upload_folder, f"leaf_{user_id or 0}_{int(os.path.getmtime(upload_folder) if os.path.exists(upload_folder) else 0)}_{filename}")
            image_file.save(saved_path)

            # Offline computer vision & ML inference
            prediction_result = self.disease_predictor.predict_from_image_path(saved_path)

            # Persist diagnosis log in database
            disease_record = self.disease_service.create_disease_record(
                farmer_id=farmer_id,
                field_id=field_id,
                image_path=saved_path,
                prediction_result=prediction_result
            )

            if user_id:
                self.audit_service.log_event(
                    user_id=user_id,
                    action="DISEASE_DIAGNOSIS_PERFORMED",
                    entity_type="DiseaseRecord",
                    entity_id=disease_record.id,
                    details={
                        "disease_name": disease_record.disease_name,
                        "confidence": disease_record.confidence_score,
                        "severity": disease_record.severity_level
                    }
                )

            serialized = self.disease_schema.dump_single(disease_record)
            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=serialized, message="Disease diagnosis completed successfully", status_code=201)

            flash(f"Diagnosis Complete: Identified '{disease_record.disease_name}' with {round(disease_record.confidence_score * 100, 1)}% confidence.", "success")
            return render_template(
                "farmer/disease_detail.html",
                record=disease_record,
                record_data=serialized,
                result=prediction_result
            )

        except Exception as e:
            return self.handle_exception(e, "Error processing leaf image diagnosis")

    def get_diagnosis_detail(self, record_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves detailed disease diagnosis record with remedies, treatment schedule, and prevention advice.
        """
        record = self.disease_service.get_record_by_id(record_id)
        if not record:
            return self.error_response(message="Disease record not found", status_code=404)

        serialized = self.disease_schema.dump_single(record)
        return self.render_or_json("farmer/disease_detail.html", {"record": record, "record_data": serialized})
