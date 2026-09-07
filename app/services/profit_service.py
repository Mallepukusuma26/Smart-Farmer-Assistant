from typing import Dict, Any, List, Optional
from app.repositories.profit_repository import ProfitRepository
from app.models.profit_prediction import ProfitPrediction
from app.models.crop import Crop
from app.models.field import Field
from ml.prediction.profit_predictor import ProfitPredictor

class ProfitService:
    """Domain Service for farm profitability prediction, what-if scenario simulations, and ROI comparison."""

    def __init__(self, repository: Optional[ProfitRepository] = None):
        self.repository = repository or ProfitRepository()
        self.predictor = ProfitPredictor()

    def predict_profit(
        self,
        farmer_id: int,
        field_id: int,
        crop_id: int,
        expected_yield_tons: float,
        expected_selling_price: float,
        estimated_expenses: float
    ) -> ProfitPrediction:
        """Forecast expected revenue, net profit, margin %, ROI %, break-even yield/price, and generate 3 scenario simulations."""
        crop = Crop.query.get(crop_id)
        field = Field.query.get(field_id)

        crop_name = crop.name if crop else 'Maize'
        area = field.area if field else 1.0

        res = self.predictor.predict(
            crop=crop_name,
            area_acres=area,
            yield_tons=float(expected_yield_tons),
            selling_price_per_ton=float(expected_selling_price),
            estimated_expenses=float(estimated_expenses)
        )

        expected_rev = float(res.get('expected_revenue', expected_yield_tons * expected_selling_price))
        expected_prof = float(res.get('expected_profit', expected_rev - estimated_expenses))

        risk = 'High' if expected_prof < 0 or estimated_expenses > expected_rev * 0.8 else ('Moderate' if estimated_expenses > expected_rev * 0.6 else 'Low')

        prediction = self.repository.save_profit_forecast(
            farmer_id=farmer_id,
            field_id=field_id,
            crop_id=crop_id,
            expected_yield_tons=float(expected_yield_tons),
            expected_selling_price=float(expected_selling_price),
            estimated_expenses=float(estimated_expenses),
            risk_level=risk
        )

        # 1. Best Case (+20% market price surge)
        best_rev = round(expected_rev * 1.20, 2)
        best_prof = round(best_rev - estimated_expenses, 2)
        self.repository.add_scenario_simulation(
            prediction_id=prediction.id,
            scenario_type='Best Case',
            price_multiplier=1.20,
            yield_multiplier=1.0,
            projected_revenue=best_rev,
            projected_profit=best_prof
        )

        # 2. Base Case (Expected standard projection)
        self.repository.add_scenario_simulation(
            prediction_id=prediction.id,
            scenario_type='Base Case',
            price_multiplier=1.0,
            yield_multiplier=1.0,
            projected_revenue=expected_rev,
            projected_profit=expected_prof
        )

        # 3. Worst Case (-25% drought yield hit)
        worst_yield = float(expected_yield_tons) * 0.75
        worst_rev = round(worst_yield * expected_selling_price, 2)
        worst_prof = round(worst_rev - estimated_expenses, 2)
        self.repository.add_scenario_simulation(
            prediction_id=prediction.id,
            scenario_type='Worst Case',
            price_multiplier=1.0,
            yield_multiplier=0.75,
            projected_revenue=worst_rev,
            projected_profit=worst_prof
        )

        return prediction

    def compare_crop_roi(self, field_id: int, crop_a_id: int, crop_b_id: int, estimated_expenses_a: float, estimated_expenses_b: float, yield_a_tons: float, yield_b_tons: float, price_a: float, price_b: float) -> Dict[str, Any]:
        """Compare expected ROI between 2 crop choices for a field plot."""
        crop_a = Crop.query.get(crop_a_id)
        crop_b = Crop.query.get(crop_b_id)

        crop_a_name = crop_a.name if crop_a else "Crop A"
        crop_b_name = crop_b.name if crop_b else "Crop B"

        rev_a = yield_a_tons * price_a
        prof_a = rev_a - estimated_expenses_a
        roi_a = round((prof_a / estimated_expenses_a) * 100.0, 2) if estimated_expenses_a > 0 else 0.0

        rev_b = yield_b_tons * price_b
        prof_b = rev_b - estimated_expenses_b
        roi_b = round((prof_b / estimated_expenses_b) * 100.0, 2) if estimated_expenses_b > 0 else 0.0

        recommendation = crop_a_name if roi_a >= roi_b else crop_b_name

        self.repository.record_roi_comparison(
            field_id=field_id,
            crop_a_name=crop_a_name,
            crop_a_roi=roi_a,
            crop_b_name=crop_b_name,
            crop_b_roi=roi_b,
            recommended_option=recommendation
        )

        return {
            'crop_a': {'name': crop_a_name, 'revenue': rev_a, 'profit': prof_a, 'roi_pct': roi_a},
            'crop_b': {'name': crop_b_name, 'revenue': rev_b, 'profit': prof_b, 'roi_pct': roi_b},
            'recommended_choice': recommendation
        }
