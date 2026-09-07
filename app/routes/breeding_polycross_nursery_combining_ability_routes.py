"""
BreedingPolycrossNurseryCombiningAbilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.breeding_polycross_nursery_combining_ability_controller import BreedingPolycrossNurseryCombiningAbilityEngineController

breeding_polycross_nursery_combining_ability_bp = Blueprint("breeding-polycross-nursery-combining-ability", __name__, url_prefix="/api/breeding-polycross-nursery-combining-ability")
controller = BreedingPolycrossNurseryCombiningAbilityEngineController()

@breeding_polycross_nursery_combining_ability_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@breeding_polycross_nursery_combining_ability_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@breeding_polycross_nursery_combining_ability_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
