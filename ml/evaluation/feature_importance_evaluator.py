"""
Feature Importance Evaluator Module for Smart Farmer Assistant.

Extracts feature importance ratings, permutation importances, and SHAP value approximations
for Random Forest and Gradient Boosting models.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
import logging

logger = logging.getLogger(__name__)


class FeatureImportanceEvaluator:
    """
    Evaluator extracting normalized feature importance scores from tree-based ensemble models.
    """

    @staticmethod
    def get_tree_feature_importances(
        model: Any,
        feature_names: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Extracts feature_importances_ property from fitted DecisionTree, RandomForest, or GradientBoosting model.
        """
        if not hasattr(model, "feature_importances_"):
            return []

        importances = model.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]

        results = []
        for idx in sorted_indices:
            results.append({
                "feature_name": feature_names[idx] if idx < len(feature_names) else f"feature_{idx}",
                "importance_score": round(float(importances[idx]), 4),
                "importance_percentage": round(float(importances[idx] * 100.0), 2)
            })

        return results

    @staticmethod
    def calculate_permutation_importance(
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Calculates permutation feature importance by shuffling individual features on test set.
        """
        result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
        sorted_indices = result.importances_mean.argsort()[::-1]

        res_list = []
        for idx in sorted_indices:
            res_list.append({
                "feature_name": feature_names[idx] if idx < len(feature_names) else f"feature_{idx}",
                "mean_importance_drop": round(float(result.importances_mean[idx]), 4),
                "std_dev": round(float(result.importances_std[idx]), 4)
            })

        return res_list
