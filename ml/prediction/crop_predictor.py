import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

class CropPredictor:
    """Prediction service for ML crop recommendation."""
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

    def predict(self, n, p, k, temperature, humidity, ph, rainfall):
        """Predict top recommended crops with suitability scores."""
        if self.model is None:
            self._load_artifacts()

        input_data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
        input_scaled = self.scaler.transform(input_data)

        probabilities = self.model.predict_proba(input_scaled)[0]
        top_indices = np.argsort(probabilities)[::-1][:3]

        results = []
        for idx in top_indices:
            crop_name = str(self.label_encoder.inverse_transform([idx])[0])
            prob = float(probabilities[idx])
            suitability_score = round(prob * 100, 1)

            # Generate natural language rationale
            reasons = []
            if 6.0 <= ph <= 7.5:
                reasons.append("Soil pH is optimal")
            if n >= 60:
                reasons.append("Adequate soil nitrogen")
            if rainfall >= 100:
                reasons.append("Favorable rainfall conditions")
            if not reasons:
                reasons.append("Matches agro-climatic profile")

            results.append({
                'crop_name': crop_name,
                'suitability_score': max(suitability_score, 15.0),
                'probability': prob,
                'reason': ", ".join(reasons),
                'required_conditions': f"N:{n}, P:{p}, K:{k}, Temp:{temperature}°C, pH:{ph}"
            })

        return results
