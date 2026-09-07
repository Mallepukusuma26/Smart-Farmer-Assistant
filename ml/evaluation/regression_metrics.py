"""
Regression Metrics Evaluator Module for Smart Farmer Assistant.

Calculates regression metrics: R2 Score, Mean Absolute Error (MAE),
Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE),
and residual distribution statistics.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import logging

logger = logging.getLogger(__name__)


class RegressionMetricsEvaluator:
    """
    Evaluates regression model predictions against actual values.
    """

    @staticmethod
    def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """
        Computes R2, MAE, RMSE, MAPE, and residual summary statistics.
        """
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        # Avoid zero division in MAPE
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if np.any(mask) else 0.0

        residuals = y_true - y_pred
        res_mean = np.mean(residuals)
        res_std = np.std(residuals)

        return {
            "r2_score": round(float(r2), 4),
            "mae": round(float(mae), 4),
            "rmse": round(float(rmse), 4),
            "mape_pct": round(float(mape), 2),
            "residual_mean": round(float(res_mean), 4),
            "residual_std": round(float(res_std), 4)
        }
