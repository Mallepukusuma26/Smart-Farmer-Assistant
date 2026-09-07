from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.profit_prediction import ProfitPrediction, ProfitScenario, ROIAnalysis
from app.repositories.base_repository import BaseRepository

class ProfitRepository(BaseRepository[ProfitPrediction]):
    """Data Access Repository for Farm Profitability Predictions, ROI Analyses, and What-if Scenarios."""

    def __init__(self):
        super().__init__(ProfitPrediction)

    def save_profit_forecast(self, farmer_id: int, field_id: int, crop_id: int, expected_yield_tons: float, expected_selling_price: float, estimated_expenses: float, risk_level: str = 'Low') -> ProfitPrediction:
        """Save profit forecast computation."""
        pred = ProfitPrediction(
            farmer_id=farmer_id,
            field_id=field_id,
            crop_id=crop_id,
            expected_yield_tons=expected_yield_tons,
            expected_selling_price=expected_selling_price,
            estimated_expenses=estimated_expenses,
            risk_level=risk_level
        )
        pred.compute_financials()
        db.session.add(pred)
        db.session.commit()
        return pred

    def get_forecasts_by_farmer(self, farmer_id: int) -> List[ProfitPrediction]:
        """Fetch all profit predictions for a farmer."""
        return db.session.query(ProfitPrediction).filter_by(farmer_id=farmer_id).order_by(ProfitPrediction.created_at.desc()).all()

    def add_scenario_simulation(self, prediction_id: int, scenario_type: str, price_multiplier: float, yield_multiplier: float, projected_revenue: float, projected_profit: float) -> ProfitScenario:
        """Add what-if scenario simulation (Best Case, Base Case, Worst Case)."""
        scen = ProfitScenario(
            prediction_id=prediction_id,
            scenario_type=scenario_type,
            price_multiplier=price_multiplier,
            yield_multiplier=yield_multiplier,
            projected_revenue=projected_revenue,
            projected_profit=projected_profit
        )
        db.session.add(scen)
        db.session.commit()
        return scen

    def record_roi_comparison(self, field_id: int, crop_a_name: str, crop_a_roi: float, crop_b_name: str, crop_b_roi: float, recommended_option: str) -> ROIAnalysis:
        """Record comparative ROI analysis between two crop alternatives."""
        roi = ROIAnalysis(
            field_id=field_id,
            crop_a_name=crop_a_name,
            crop_a_roi_pct=crop_a_roi,
            crop_b_name=crop_b_name,
            crop_b_roi_pct=crop_b_roi,
            recommended_option=recommended_option
        )
        db.session.add(roi)
        db.session.commit()
        return roi
