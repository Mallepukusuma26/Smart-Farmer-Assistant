"""
EnergyBiogasAnaerobicDigesterYieldEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.energy_biogas_anaerobic_digester_yield_controller import EnergyBiogasAnaerobicDigesterYieldEngineController

energy_biogas_anaerobic_digester_yield_bp = Blueprint("energy-biogas-anaerobic-digester-yield", __name__, url_prefix="/api/energy-biogas-anaerobic-digester-yield")
controller = EnergyBiogasAnaerobicDigesterYieldEngineController()

@energy_biogas_anaerobic_digester_yield_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@energy_biogas_anaerobic_digester_yield_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@energy_biogas_anaerobic_digester_yield_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
