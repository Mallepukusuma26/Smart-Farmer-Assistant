"""
BreedingHybridSeedPurityIsolationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.breeding_hybrid_seed_purity_isolation_controller import BreedingHybridSeedPurityIsolationEngineController

breeding_hybrid_seed_purity_isolation_bp = Blueprint("breeding-hybrid-seed-purity-isolation", __name__, url_prefix="/api/breeding-hybrid-seed-purity-isolation")
controller = BreedingHybridSeedPurityIsolationEngineController()

@breeding_hybrid_seed_purity_isolation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@breeding_hybrid_seed_purity_isolation_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@breeding_hybrid_seed_purity_isolation_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
