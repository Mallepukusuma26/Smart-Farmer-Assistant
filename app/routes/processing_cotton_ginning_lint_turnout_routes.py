"""
ProcessingCottonGinningLintTurnoutEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.processing_cotton_ginning_lint_turnout_controller import ProcessingCottonGinningLintTurnoutEngineController

processing_cotton_ginning_lint_turnout_bp = Blueprint("processing-cotton-ginning-lint-turnout", __name__, url_prefix="/api/processing-cotton-ginning-lint-turnout")
controller = ProcessingCottonGinningLintTurnoutEngineController()

@processing_cotton_ginning_lint_turnout_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@processing_cotton_ginning_lint_turnout_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@processing_cotton_ginning_lint_turnout_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
