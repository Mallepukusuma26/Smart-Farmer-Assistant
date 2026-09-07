"""
Advisor Controller Module for Smart Farmer Assistant.

Manages agricultural advisor profiles, farmer consultation requests, advisory case notes,
field visit logs, expert crop/soil/fertilizer recommendations, and consultation history tracking.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.advisor_service import AdvisorService
from app.services.farmer_service import FarmerService
from app.services.farm_service import FarmService
from app.services.audit_service import AuditService
from app.schemas.advisor_schema import AdvisorSchema, AdvisorCaseSchema
import logging

logger = logging.getLogger(__name__)


class AdvisorController(BaseController):
    """
    Controller providing agricultural advisor portal, farmer case assignment,
    consultation note submission, advice history, and expert recommendations.
    """

    def __init__(self):
        self.advisor_service = AdvisorService()
        self.farmer_service = FarmerService()
        self.farm_service = FarmService()
        self.audit_service = AuditService()
        self.advisor_schema = AdvisorSchema()
        self.case_schema = AdvisorCaseSchema()

    def dashboard(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders the Agricultural Advisor Workspace dashboard displaying pending farmer requests,
        assigned cases, recent recommendations, and high-priority field disease alerts.
        """
        user_id = self.get_current_user_id()
        if not user_id or not (self.is_advisor() or self.is_admin()):
            return redirect(url_for("auth.login"))

        advisor = self.advisor_service.get_advisor_by_user_id(user_id)
        if not advisor:
            advisor = self.advisor_service.create_advisor_profile_for_user(user_id)

        cases = self.advisor_service.get_cases_by_advisor(advisor.id)
        open_cases = [c for c in cases if c.status == "open"]
        pending_cases = [c for c in cases if c.status == "pending"]
        completed_cases = [c for c in cases if c.status == "resolved"]

        dashboard_data = {
            "advisor": self.advisor_schema.dump_single(advisor),
            "total_cases": len(cases),
            "open_cases_count": len(open_cases),
            "pending_cases_count": len(pending_cases),
            "completed_cases_count": len(completed_cases),
            "recent_cases": self.case_schema.dump_list(cases[:10])
        }

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=dashboard_data)

        return render_template("advisor/dashboard.html", **dashboard_data)

    def list_cases(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists advisory cases submitted by farmers.
        """
        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        user_id = self.get_current_user_id()
        if self.is_farmer():
            farmer = self.farmer_service.get_farmer_by_user_id(user_id)
            if not farmer:
                cases, total = [], 0
            else:
                cases, total = self.advisor_service.get_cases_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)
        else:
            cases, total = self.advisor_service.get_all_cases_paginated(page=page, per_page=per_page, filters=filters)

        serialized = self.case_schema.dump_list(cases)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "advisor/cases.html",
            cases=cases,
            cases_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def create_case(self) -> Union[str, Tuple[Response, int]]:
        """
        Farmer endpoint to request expert advisory consultation regarding crop disease, soil, or yield issues.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            farmer = self.farmer_service.create_farmer_profile_for_user(user_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        data["farmer_id"] = farmer.id

        subject = data.get("subject", "").strip()
        description = data.get("description", "").strip()
        if not subject or not description:
            msg = "Subject and description are required"
            if request.is_json:
                return self.error_response(message=msg, status_code=400)
            flash(msg, "danger")
            return redirect(url_for("farmer.list_cases"))

        try:
            case = self.advisor_service.create_case(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="ADVISORY_CASE_CREATED",
                entity_type="AdvisorCase",
                entity_id=case.id,
                details={"subject": case.subject}
            )

            serialized = self.case_schema.dump_single(case)
            if request.is_json:
                return self.success_response(data=serialized, message="Advisory case created successfully", status_code=201)

            flash("Advisory ticket submitted! An agricultural advisor will review it shortly.", "success")
            return redirect(url_for("advisor.list_cases"))

        except Exception as e:
            return self.handle_exception(e, "Error creating advisory case")

    def resolve_case(self, case_id: int) -> Union[str, Tuple[Response, int]]:
        """
        Advisor endpoint to record expert resolution advice, treatment recommendation, and mark case resolved.
        """
        if not (self.is_advisor() or self.is_admin()):
            return self.error_response(message="Advisor access required", status_code=403)

        data = request.get_json() if request.is_json else request.form.to_dict()
        advice = data.get("recommendation", data.get("advice", "")).strip()

        if not advice:
            msg = "Expert advice text is required"
            if request.is_json:
                return self.error_response(message=msg, status_code=400)
            flash(msg, "danger")
            return redirect(url_for("advisor.get_case_detail", case_id=case_id))

        try:
            user_id = self.get_current_user_id()
            advisor = self.advisor_service.get_advisor_by_user_id(user_id)

            resolved_case = self.advisor_service.resolve_case(
                case_id=case_id,
                advisor_id=advisor.id if advisor else None,
                recommendation=advice
            )

            self.audit_service.log_event(
                user_id=user_id,
                action="ADVISORY_CASE_RESOLVED",
                entity_type="AdvisorCase",
                entity_id=case_id
            )

            serialized = self.case_schema.dump_single(resolved_case)
            if request.is_json:
                return self.success_response(data=serialized, message="Case resolved successfully")

            flash("Advice submitted and case resolved!", "success")
            return redirect(url_for("advisor.list_cases"))

        except Exception as e:
            return self.handle_exception(e, "Error resolving advisory case")
