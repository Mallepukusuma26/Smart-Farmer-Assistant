from datetime import datetime
import json
from app.extensions import db

class YieldPrediction(db.Model):
    """Yield prediction inference result for a field."""
    __tablename__ = 'yield_predictions'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    predicted_yield_tons = db.Column(db.Float, nullable=False)
    expected_range_min = db.Column(db.Float, nullable=False)
    expected_range_max = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, default=0.88)
    parameters_json = db.Column(db.Text, nullable=True) # Input feature dictionary JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_parameters(self):
        if self.parameters_json:
            try:
                return json.loads(self.parameters_json)
            except Exception:
                return {}
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'predicted_yield_tons': round(self.predicted_yield_tons, 2),
            'expected_range_min': round(self.expected_range_min, 2),
            'expected_range_max': round(self.expected_range_max, 2),
            'confidence_score': self.confidence_score,
            'parameters': self.get_parameters(),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<YieldPrediction id={self.id} crop_id={self.crop_id} yield={self.predicted_yield_tons}>"
