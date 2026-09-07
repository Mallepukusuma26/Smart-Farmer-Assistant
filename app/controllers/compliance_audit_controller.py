"""
Compliance Audit Controller Module for Smart Farmer Assistant.

Manages environmental safety audits, groundwater nitrate leaching evaluation, and GAP compliance.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.compliance_audit_service import ComplianceAuditService
import logging

logger = logging.getLogger(__name__)


class ComplianceAuditController(BaseController):
    """
    Controller executing GAP compliance audits and environmental safety checks.
    """

    def __init__(self):
        self.audit_service = ComplianceAuditService()

    def audit_nitrate(self) -> Union[str, Tuple[Response, int]]:
        """
        Evaluates potential nitrate leaching risk into groundwater reserves.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        applied_n = float(data.get("applied_nitrogen_kg_acre", 60.0))
        uptake_n = float(data.get("crop_n_uptake_kg_acre", 45.0))
        over_irrig = float(data.get("irrigation_over_application_pct", 10.0))
        sand = float(data.get("soil_sand_pct", 40.0))

        res = self.audit_service.audit_nitrate_leaching_risk(applied_n, uptake_n, over_irrig, sand)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("admin/compliance_audit.html", result=res)
