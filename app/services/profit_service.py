from app.extensions import db
from app.models.profit_prediction import ProfitPrediction
from app.models.crop import Crop
from app.models.field import Field
from ml.prediction.profit_predictor import ProfitPredictor

class ProfitService:
    """Service layer for farm profit forecasting engine."""

    predictor = ProfitPredictor()

    @staticmethod
    def predict_profit(farmer_id, field_id, crop_id, expected_yield_tons, expected_selling_price, estimated_expenses):
        """Predict expected revenue, net profit, margin, and break-even points."""
        crop = Crop.query.get(crop_id)
        field = Field.query.get(field_id)

        crop_name = crop.name if crop else 'Maize'
        area = field.area if field else 1.0

        res = ProfitService.predictor.predict(
            crop=crop_name,
            area_acres=area,
            yield_tons=float(expected_yield_tons),
            selling_price_per_ton=float(expected_selling_price),
            estimated_expenses=float(estimated_expenses)
        )

        prediction = ProfitPrediction(
            farmer_id=farmer_id,
            field_id=field_id,
            crop_id=crop_id,
            expected_yield_tons=float(expected_yield_tons),
            expected_selling_price=float(expected_selling_price),
            estimated_expenses=float(estimated_expenses),
            expected_revenue=res['expected_revenue'],
            expected_profit=res['expected_profit'],
            profit_margin_percent=res['profit_margin_percent'],
            break_even_yield=res['break_even_yield_tons']
        )

        db.session.add(prediction)
        db.session.commit()
        return prediction
