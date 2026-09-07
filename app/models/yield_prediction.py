from datetime import datetime
import json
from typing import Dict, Any, List, Optional
from app.extensions import db

class YieldPrediction(db.Model):
    """Yield prediction inference result for a field based on local ML regressors."""
    __tablename__ = 'yield_predictions'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    model_name_used = db.Column(db.String(100), default='Random Forest Regressor')
    predicted_yield_tons = db.Column(db.Float, nullable=False)
    yield_per_acre_tons = db.Column(db.Float, nullable=False, default=2.5)
    expected_range_min = db.Column(db.Float, nullable=False)
    expected_range_max = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, default=0.88) # R-squared metric indicator
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    crop = db.relationship('Crop')

    def get_parameters(self) -> Dict[str, Any]:
        """Parse stored feature parameters JSON safely."""
        if self.parameters_json:
            try:
                return json.loads(self.parameters_json)
            except Exception:
                return {}
        return {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'model_name_used': self.model_name_used,
            'predicted_yield_tons': round(self.predicted_yield_tons, 2),
            'yield_per_acre_tons': round(self.yield_per_acre_tons, 2),
            'expected_range_min': round(self.expected_range_min, 2),
            'expected_range_max': round(self.expected_range_max, 2),
            'confidence_score': self.confidence_score,
            'parameters': self.get_parameters(),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<YieldPrediction id={self.id} crop_id={self.crop_id} yield={self.predicted_yield_tons}>"


class YieldRecord(db.Model):
    """Actual historical harvest outcome recorded after crop harvest."""
    __tablename__ = 'yield_records'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('crop_cycles.id', ondelete='SET NULL'), nullable=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('yield_predictions.id', ondelete='SET NULL'), nullable=True)
    harvest_date = db.Column(db.Date, nullable=False)
    actual_yield_tons = db.Column(db.Float, nullable=False)
    quality_grade = db.Column(db.String(30), default='Grade A') # Grade A, Grade B, Grade C
    market_price_per_ton = db.Column(db.Float, default=0.0)
    total_revenue_generated = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    field = db.relationship('Field', backref=db.backref('yield_records', lazy='dynamic', cascade='all, delete-orphan'))
    crop = db.relationship('Crop', backref=db.backref('yield_records', lazy='dynamic'))

    def calculate_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy ratio against predicted_yield_tons if linked."""
        if not self.prediction_id:
            return 100.0
        pred = YieldPrediction.query.get(self.prediction_id)
        if not pred or pred.predicted_yield_tons <= 0:
            return 100.0
        diff = abs(self.actual_yield_tons - pred.predicted_yield_tons)
        accuracy = max(0.0, (1.0 - (diff / pred.predicted_yield_tons))) * 100.0
        return round(accuracy, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'harvest_date': self.harvest_date.strftime('%Y-%m-%d') if self.harvest_date else None,
            'actual_yield_tons': round(self.actual_yield_tons, 2),
            'quality_grade': self.quality_grade,
            'market_price_per_ton': self.market_price_per_ton,
            'total_revenue_generated': self.total_revenue_generated,
            'accuracy_pct': self.calculate_prediction_accuracy(),
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<YieldRecord id={self.id} actual_yield={self.actual_yield_tons}>"


class YieldFactor(db.Model):
    """Environmental and agronomic feature weights affecting crop productivity."""
    __tablename__ = 'yield_factors'

    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('yield_predictions.id', ondelete='CASCADE'), nullable=False)
    factor_name = db.Column(db.String(100), nullable=False) # Soil NPK, Rainfall, Temperature, Irrigation Efficiency
    impact_pct = db.Column(db.Float, nullable=False, default=0.0) # Feature importance contribution (+/-)
    status_impact = db.Column(db.String(30), default='Positive') # Positive, Neutral, Limiting

    prediction = db.relationship('YieldPrediction', backref=db.backref('factors', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'prediction_id': self.prediction_id,
            'factor_name': self.factor_name,
            'impact_pct': self.impact_pct,
            'status_impact': self.status_impact
        }


class HistoricalYieldBenchmark(db.Model):
    """Regional historical crop productivity benchmarks by agro-climatic zone."""
    __tablename__ = 'historical_yield_benchmarks'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    district_region = db.Column(db.String(100), nullable=False)
    avg_yield_tons_per_acre = db.Column(db.Float, nullable=False)
    max_yield_tons_per_acre = db.Column(db.Float, nullable=False)
    min_yield_tons_per_acre = db.Column(db.Float, nullable=False)
    recorded_year = db.Column(db.Integer, default=2024)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'district_region': self.district_region,
            'avg_yield_tons_per_acre': self.avg_yield_tons_per_acre,
            'max_yield_tons_per_acre': self.max_yield_tons_per_acre,
            'min_yield_tons_per_acre': self.min_yield_tons_per_acre,
            'recorded_year': self.recorded_year
        }

