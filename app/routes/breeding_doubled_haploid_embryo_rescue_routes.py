"""
BreedingDoubledHaploidEmbryoRescueEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.breeding_doubled_haploid_embryo_rescue_controller import BreedingDoubledHaploidEmbryoRescueEngineController

breeding_doubled_haploid_embryo_rescue_bp = Blueprint("breeding-doubled-haploid-embryo-rescue", __name__, url_prefix="/api/breeding-doubled-haploid-embryo-rescue")
controller = BreedingDoubledHaploidEmbryoRescueEngineController()

@breeding_doubled_haploid_embryo_rescue_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@breeding_doubled_haploid_embryo_rescue_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@breeding_doubled_haploid_embryo_rescue_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
