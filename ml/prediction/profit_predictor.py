import os
import joblib
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

class ProfitPredictor:
    """Predictor service for farm financial profit forecasting."""
    def __init__(self):
        self.model = None
        self.encoder = None
        self.scaler = None
        self._load_artifacts()

    def _load_artifacts(self):
        m_path = os.path.join(MODEL_DIR, 'profit_model.joblib')
        e_path = os.path.join(MODEL_DIR, 'profit_crop_encoder.joblib')
        s_path = os.path.join(MODEL_DIR, 'profit_scaler.joblib')
        if os.path.exists(m_path):
            self.model = joblib.load(m_path)
        if os.path.exists(e_path):
            self.encoder = joblib.load(e_path)
        if os.path.exists(s_path):
            self.scaler = joblib.load(s_path)

    def predict(self, crop, area_acres, yield_tons, selling_price_per_ton, estimated_expenses):
        """Predict expected revenue, expenses, net profit, margin, and break-even point."""
        expected_revenue = yield_tons * selling_price_per_ton
        expected_profit = expected_revenue - estimated_expenses

        profit_margin_percent = (expected_profit / max(expected_revenue, 1.0)) * 100.0
        break_even_yield = estimated_expenses / max(selling_price_per_ton, 1.0)

        return {
            'expected_revenue': round(expected_revenue, 2),
            'estimated_expenses': round(estimated_expenses, 2),
            'expected_profit': round(expected_profit, 2),
            'profit_margin_percent': round(profit_margin_percent, 2),
            'break_even_yield_tons': round(break_even_yield, 2),
            'break_even_price_per_ton': round(estimated_expenses / max(yield_tons, 0.1), 2)
        }
