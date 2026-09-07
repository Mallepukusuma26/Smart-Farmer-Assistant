"""
Batch Inference Service Module for Smart Farmer Assistant.

Provides high-throughput offline batch inference execution across large datasets
for Crop Recommendation, Yield Regression, and Farm Profitability.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import logging

from ml.prediction.crop_predictor import CropPredictor
from ml.prediction.yield_predictor import YieldPredictor
from ml.prediction.profit_predictor import ProfitPredictor

logger = logging.getLogger(__name__)


class BatchInferenceService:
    """
    Executes batch machine learning inference on pandas DataFrames or lists of record dictionaries.
    """

    def __init__(self):
        self.crop_predictor = CropPredictor()
        self.yield_predictor = YieldPredictor()
        self.profit_predictor = ProfitPredictor()

    def run_crop_batch_inference(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs batch crop recommendation inference for multiple field soil samples.
        """
        results = []
        for rec in records:
            N = float(rec.get("N", 50))
            P = float(rec.get("P", 50))
            K = float(rec.get("K", 50))
            temp = float(rec.get("temperature", 25.0))
            hum = float(rec.get("humidity", 65.0))
            ph = float(rec.get("ph", 6.5))
            rain = float(rec.get("rainfall", 100.0))

            top_crops = self.crop_predictor.predict_top_n(N, P, K, temp, hum, ph, rain, top_n=3)
            results.append({
                "input_record": rec,
                "top_recommendation": top_crops[0]["crop_name"] if top_crops else "Unknown",
                "top_confidence": top_crops[0]["confidence"] if top_crops else 0.0,
                "top_3_recommendations": top_crops
            })
        return results

    def run_yield_batch_inference(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs batch crop yield regression inference.
        """
        results = []
        for rec in records:
            crop_name = rec.get("crop_name", "rice")
            rain = float(rec.get("rainfall_mm", 1000.0))
            pest = float(rec.get("pesticides_tonnes", 0.5))
            temp = float(rec.get("avg_temp", 26.0))
            area = float(rec.get("area_acres", 1.0))

            yield_per_acre = self.yield_predictor.predict_yield(crop_name, rain, pest, temp)
            results.append({
                "input_record": rec,
                "predicted_yield_per_acre_tonnes": round(yield_per_acre, 2),
                "total_expected_yield_tonnes": round(yield_per_acre * area, 2)
            })
        return results
