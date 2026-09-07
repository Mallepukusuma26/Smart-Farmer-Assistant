import os
import math
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

class CropPredictor:
    """Prediction service for ML crop recommendation with input sanitization and fallback support."""
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self._load_artifacts()

    def _load_artifacts(self):
        model_path = os.path.join(MODEL_DIR, 'crop_model.joblib')
        scaler_path = os.path.join(MODEL_DIR, 'crop_scaler.joblib')
        encoder_path = os.path.join(MODEL_DIR, 'crop_label_encoder.joblib')

        if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(encoder_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoder = joblib.load(encoder_path)

    def _sanitize_val(self, val, default_val=0.0, min_val=0.0):
        """Sanitizes numerical inputs against NaN, Inf, or negative values."""
        try:
            num = float(val)
            if math.isnan(num) or math.isinf(num):
                return default_val
            return max(min_val, num)
        except (ValueError, TypeError):
            return default_val

    def predict_top_n(self, n, p, k, temperature, humidity, ph, rainfall, top_n: int = 3):
        """Returns top N recommendations in dictionary format suitable for batch inference."""
        recs = self.predict(n, p, k, temperature, humidity, ph, rainfall)
        formatted = []
        for r in recs[:top_n]:
            formatted.append({
                "crop_name": r["crop_name"],
                "confidence": round(r["probability"], 3),
                "suitability_score": r["suitability_score"],
                "reason": r["reason"]
            })
        return formatted

    def predict(self, n, p, k, temperature, humidity, ph, rainfall):
        """Predict top recommended crops with suitability scores and input validation."""
        if self.model is None:
            self._load_artifacts()

        # Sanitize numerical inputs
        n_val = self._sanitize_val(n, 50.0, 0.0)
        p_val = self._sanitize_val(p, 50.0, 0.0)
        k_val = self._sanitize_val(k, 50.0, 0.0)
        temp_val = self._sanitize_val(temperature, 25.0, 0.0)
        hum_val = self._sanitize_val(humidity, 65.0, 0.0)
        ph_val = self._sanitize_val(ph, 6.5, 3.0)
        rain_val = self._sanitize_val(rainfall, 100.0, 0.0)

        prediction_source = "agronomic_rule_engine"

        if self.model and self.scaler and self.label_encoder:
            try:
                input_data = np.array([[n_val, p_val, k_val, temp_val, hum_val, ph_val, rain_val]])
                input_scaled = self.scaler.transform(input_data)
                probabilities = self.model.predict_proba(input_scaled)[0]
                top_indices = np.argsort(probabilities)[::-1][:3]
                prediction_source = "trained_random_forest_classifier"

                results = []
                for idx in top_indices:
                    crop_name = str(self.label_encoder.inverse_transform([idx])[0])
                    prob = float(probabilities[idx])
                    suitability_score = round(prob * 100, 1)

                    reasons = []
                    if 6.0 <= ph_val <= 7.5:
                        reasons.append("Soil pH is optimal")
                    if n_val >= 60:
                        reasons.append("Adequate soil nitrogen")
                    if rain_val >= 100:
                        reasons.append("Favorable rainfall conditions")
                    if not reasons:
                        reasons.append("Matches agro-climatic profile")

                    results.append({
                        'crop_name': crop_name,
                        'suitability_score': max(suitability_score, 15.0),
                        'probability': prob,
                        'reason': ", ".join(reasons),
                        'prediction_source': prediction_source,
                        'required_conditions': f"N:{n_val}, P:{p_val}, K:{k_val}, Temp:{temp_val}°C, pH:{ph_val}"
                    })
                return results
            except Exception:
                pass

        # Fallback recommendations if ML model pipeline is unavailable
        fallback_crops = [
            ("rice" if rain_val > 150 else "maize", 0.82, "High moisture adaptation"),
            ("wheat" if temp_val < 22 else "chickpea", 0.74, "Favorable temperature regime"),
            ("cotton" if k_val > 40 else "pigeonpea", 0.65, "Soil nutrient compatibility")
        ]
        return [
            {
                'crop_name': crop,
                'suitability_score': round(prob * 100, 1),
                'probability': prob,
                'reason': reason,
                'prediction_source': prediction_source,
                'required_conditions': f"N:{n_val}, P:{p_val}, K:{k_val}, Temp:{temp_val}°C, pH:{ph_val}"
            }
            for crop, prob, reason in fallback_crops
        ]

