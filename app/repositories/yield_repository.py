from typing import Optional, List, Dict, Any, Tuple
import json
from datetime import datetime, date
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.yield_prediction import YieldPrediction, YieldRecord, YieldFactor, HistoricalYieldBenchmark
from app.repositories.base_repository import BaseRepository

class YieldRepository(BaseRepository[YieldPrediction]):
    """Data Access Repository for Yield ML Predictions, Actual Harvest Logs, and Productivity Benchmarks."""

    def __init__(self):
        super().__init__(YieldPrediction)

    def save_prediction(self, field_id: int, crop_id: int, predicted_yield_tons: float, yield_per_acre_tons: float, expected_range_min: float, expected_range_max: float, confidence_score: float = 0.88, model_name: str = 'Random Forest Regressor', parameters: Optional[Dict[str, Any]] = None) -> YieldPrediction:
        """Save local ML regressor yield prediction result."""
        params_str = json.dumps(parameters) if parameters else None
        pred = YieldPrediction(
            field_id=field_id,
            crop_id=crop_id,
            predicted_yield_tons=predicted_yield_tons,
            yield_per_acre_tons=yield_per_acre_tons,
            expected_range_min=expected_range_min,
            expected_range_max=expected_range_max,
            confidence_score=confidence_score,
            model_name_used=model_name,
            parameters_json=params_str
        )
        db.session.add(pred)
        db.session.commit()
        return pred

    def get_predictions_by_field(self, field_id: int) -> List[YieldPrediction]:
        """Fetch historical yield predictions for field."""
        return db.session.query(YieldPrediction).filter_by(field_id=field_id).order_by(YieldPrediction.created_at.desc()).all()

    def record_actual_harvest(self, field_id: int, crop_id: int, harvest_date: date, actual_yield_tons: float, crop_cycle_id: Optional[int] = None, prediction_id: Optional[int] = None, quality_grade: str = 'Grade A', market_price_per_ton: float = 0.0, notes: Optional[str] = None) -> YieldRecord:
        """Record actual harvest outcome to evaluate prediction model accuracy."""
        revenue = round(actual_yield_tons * market_price_per_ton, 2)
        rec = YieldRecord(
            field_id=field_id,
            crop_id=crop_id,
            crop_cycle_id=crop_cycle_id,
            prediction_id=prediction_id,
            harvest_date=harvest_date,
            actual_yield_tons=actual_yield_tons,
            quality_grade=quality_grade,
            market_price_per_ton=market_price_per_ton,
            total_revenue_generated=revenue,
            notes=notes
        )
        db.session.add(rec)
        db.session.commit()
        return rec

    def get_actual_harvest_records(self, field_id: Optional[int] = None, crop_id: Optional[int] = None) -> List[YieldRecord]:
        """Fetch actual harvest records."""
        query = db.session.query(YieldRecord)
        if field_id:
            query = query.filter_by(field_id=field_id)
        if crop_id:
            query = query.filter_by(crop_id=crop_id)
        return query.order_by(YieldRecord.harvest_date.desc()).all()

    def add_yield_factor(self, prediction_id: int, factor_name: str, impact_pct: float, status_impact: str = 'Positive') -> YieldFactor:
        """Attach agronomic feature importance factor to a yield prediction."""
        factor = YieldFactor(
            prediction_id=prediction_id,
            factor_name=factor_name,
            impact_pct=impact_pct,
            status_impact=status_impact
        )
        db.session.add(factor)
        db.session.commit()
        return factor

    def get_regional_benchmark(self, crop_name: str, district_region: str = 'Central Region') -> Optional[HistoricalYieldBenchmark]:
        """Fetch agro-climatic regional productivity benchmark for comparison."""
        return db.session.query(HistoricalYieldBenchmark).filter(
            func.lower(HistoricalYieldBenchmark.crop_name) == crop_name.lower().strip(),
            func.lower(HistoricalYieldBenchmark.district_region) == district_region.lower().strip()
        ).first()
