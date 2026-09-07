"""
Report Controller Module for Smart Farmer Assistant.

Manages automated generation, rendering, and downloading of multi-category agricultural reports
(Farmer Report, Farm Report, Field Report, Soil Report, Crop Recommendation Report, Fertilizer Report,
Irrigation Report, Disease Report, Yield Report, Financial Statement, Monthly/Seasonal Summaries)
supporting HTML views, CSV exports, JSON payloads, and printable PDF documents.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response, send_file
from app.controllers.base_controller import BaseController
from app.services.report_service import ReportService
from app.services.farmer_service import FarmerService
from app.services.audit_service import AuditService
from app.utils.csv_generator import CSVGenerator
from app.utils.pdf_generator import PDFGenerator
from app.schemas.report_schema import ReportSchema
import logging
import io

logger = logging.getLogger(__name__)


class ReportController(BaseController):
    """
    Controller handling report parameter extraction, multi-format rendering (HTML/CSV/JSON/PDF),
    historical report archiving, and export downloading.
    """

    def __init__(self):
        self.report_service = ReportService()
        self.farmer_service = FarmerService()
        self.audit_service = AuditService()
        self.csv_generator = CSVGenerator()
        self.pdf_generator = PDFGenerator()
        self.report_schema = ReportSchema()

    def list_reports(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists generated reports archive for the current user.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        reports, total = self.report_service.get_reports_by_user_paginated(user_id, page=page, per_page=per_page, filters=filters)
        serialized = self.report_schema.dump_list(reports)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/reports.html",
            reports=reports,
            reports_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def generate_report(self) -> Union[str, Tuple[Response, int]]:
        """
        Generates custom specified report category (farm, soil, financial, disease, yield, irrigation)
        and outputs HTML preview or downloadable CSV/JSON/PDF file.
        """
        user_id = BaseController.get_current_user_id()
        if not user_id:
            return BaseController.error_response(message="Authentication required", status_code=401)

        report_type = request.args.get("type", request.form.get("type", "financial")).strip().lower()
        export_format = request.args.get("format", request.form.get("format", "html")).strip().lower()
        date_from = request.args.get("date_from", "")
        date_to = request.args.get("date_to", "")

        farmer_service = FarmerService()
        report_service = ReportService()
        audit_service = AuditService()

        farmer = farmer_service.get_farmer_by_user_id(user_id)
        farmer_id = farmer.id if farmer else None

        try:
            report_data = report_service.compile_report_dataset(
                report_type=report_type,
                farmer_id=farmer_id,
                date_from=date_from,
                date_to=date_to
            )

            # Record generated report entry
            saved_report = report_service.create_report_record(
                user_id=user_id,
                report_type=report_type,
                title=f"{report_type.capitalize()} Report ({report_data.get('generated_at', '')})",
                format_type=export_format,
                content_json=report_data
            )

            audit_service.log_event(
                user_id=user_id,
                action="REPORT_GENERATED",
                entity_type="Report",
                entity_id=saved_report.id,
                details={"type": report_type, "format": export_format}
            )

            if export_format == "csv":
                csv_bytes = CSVGenerator().generate_csv_from_data(report_data.get("table_rows", []), report_data.get("headers", []))
                return send_file(
                    io.BytesIO(csv_bytes),
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name=f"{report_type}_report.csv"
                )

            elif export_format == "pdf":
                pdf_bytes = PDFGenerator().generate_pdf_report(report_data)
                return send_file(
                    io.BytesIO(pdf_bytes),
                    mimetype="application/pdf",
                    as_attachment=True,
                    download_name=f"{report_type}_report.pdf"
                )

            elif export_format == "json" or request.is_json:
                return BaseController.success_response(data=report_data, message="Report generated successfully")

            return render_template(
                "farmer/report_view.html",
                report=saved_report,
                report_data=report_data,
                report_type=report_type
            )

        except Exception as e:
            return BaseController.handle_exception(e, f"Error generating {report_type} report")
