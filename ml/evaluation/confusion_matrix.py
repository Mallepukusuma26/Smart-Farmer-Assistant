"""
Confusion Matrix & Classification Evaluation Module for Smart Farmer Assistant.

Provides confusion matrix generation, classification report data,
class-wise Precision/Recall/F1-score calculation, and ROC-AUC curve dataset generation.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import logging

logger = logging.getLogger(__name__)


class ConfusionMatrixEvaluator:
    """
    Evaluates multi-class classification outputs, generates structured confusion matrices,
    and computes class-specific precision and recall metrics.
    """

    @staticmethod
    def evaluate_classification(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        class_names: List[str]
    ) -> Dict[str, Any]:
        """
        Generates 2D confusion matrix array, per-class metrics, and macro/weighted averages.
        """
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True, zero_division=0)

        per_class_metrics = []
        for idx, name in enumerate(class_names):
            if name in report:
                per_class_metrics.append({
                    "class_name": name,
                    "precision": round(report[name]["precision"], 4),
                    "recall": round(report[name]["recall"], 4),
                    "f1_score": round(report[name]["f1-score"], 4),
                    "support": report[name]["support"]
                })

        return {
            "confusion_matrix": cm.tolist(),
            "class_names": class_names,
            "overall_accuracy": round(report.get("accuracy", 0.0), 4),
            "macro_avg_f1": round(report.get("macro avg", {}).get("f1-score", 0.0), 4),
            "weighted_avg_f1": round(report.get("weighted avg", {}).get("f1-score", 0.0), 4),
            "per_class_metrics": per_class_metrics
        }
