"""
Crop Phenology Controller Module for Smart Farmer Assistant.

Manages BBCH growth scale predictions and accumulated Growing Degree Days (GDD) tracking.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.crop_phenology_service import CropPhenologyService
import logging

logger = logging.getLogger(__name__)


class CropPhenologyController(BaseController):
    """
    Controller handling crop growth stage predictions and GDD accumulation tracking.
    """

    def __init__(self):
        self.pheno_service = CropPhenologyService()

    def predict_growth_stage(self) -> Union[str, Tuple[Response, int]]:
        """
        Predicts BBCH growth stage from crop name and accumulated GDD.
        """
        crop_name = request.args.get("crop_name", request.form.get("crop_name", "rice"))
        gdd = float(request.args.get("gdd", request.form.get("gdd", 650.0)))

        res = self.pheno_service.predict_bbch_growth_stage(crop_name, gdd)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/crop_phenology.html", result=res)
