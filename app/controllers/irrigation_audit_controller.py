"""
Irrigation Audit Controller Module for Smart Farmer Assistant.

Manages Christiansen Uniformity Coefficient (CU %) calculations and Hazen-Williams friction loss evaluation.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.irrigation_audit_service import IrrigationAuditService
import logging

logger = logging.getLogger(__name__)


class IrrigationAuditController(BaseController):
    """
    Controller auditing drip and sprinkler irrigation system uniformity.
    """

    def __init__(self):
        self.audit_service = IrrigationAuditService()

    def audit_uniformity(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Christiansen Uniformity (CU %) from catch can data.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        volumes = data.get("volumes", [100.0, 95.0, 105.0, 98.0, 102.0, 90.0, 110.0, 95.0])

        res = self.audit_service.calculate_christiansen_uniformity(volumes)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/irrigation_audit.html", result=res)
