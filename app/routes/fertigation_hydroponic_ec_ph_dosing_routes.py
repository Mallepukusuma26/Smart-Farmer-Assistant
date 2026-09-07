"""
FertigationHydroponicECpHDosingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertigation_hydroponic_ec_ph_dosing_controller import FertigationHydroponicECpHDosingEngineController

fertigation_hydroponic_ec_ph_dosing_bp = Blueprint("fertigation-hydroponic-ec-ph-dosing", __name__, url_prefix="/api/fertigation-hydroponic-ec-ph-dosing")
controller = FertigationHydroponicECpHDosingEngineController()

@fertigation_hydroponic_ec_ph_dosing_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@fertigation_hydroponic_ec_ph_dosing_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@fertigation_hydroponic_ec_ph_dosing_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
