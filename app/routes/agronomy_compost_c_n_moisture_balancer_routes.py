"""
AgronomyCompostCNMoistureBalancerEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_compost_c_n_moisture_balancer_controller import AgronomyCompostCNMoistureBalancerEngineController

agronomy_compost_c_n_moisture_balancer_bp = Blueprint("agronomy-compost-c-n-moisture-balancer", __name__, url_prefix="/api/agronomy-compost-c-n-moisture-balancer")
ctrl = AgronomyCompostCNMoistureBalancerEngineController()

@agronomy_compost_c_n_moisture_balancer_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
