"""
AgronomyPestThermalDegreeDayModelEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_pest_thermal_degree_day_model_controller import AgronomyPestThermalDegreeDayModelEngineController

agronomy_pest_thermal_degree_day_model_bp = Blueprint("agronomy-pest-thermal-degree-day-model", __name__, url_prefix="/api/agronomy-pest-thermal-degree-day-model")
ctrl = AgronomyPestThermalDegreeDayModelEngineController()

@agronomy_pest_thermal_degree_day_model_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
