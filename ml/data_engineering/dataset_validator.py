"""
Dataset Validator Module for Smart Farmer Assistant.

Provides data integrity rules, range checking, schema validation,
and anomaly detection for agricultural training datasets.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DatasetValidator:
    """
    Validates CSV datasets against expected numerical ranges and categorical enum domains.
    """

    @staticmethod
    def validate_crop_dataset_ranges(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates N, P, K, temperature, humidity, pH, and rainfall numerical range boundaries.
        """
        errors = []
        warnings = []

        ranges = {
            "N": (0, 300),
            "P": (0, 300),
            "K": (0, 300),
            "temperature": (-10, 60),
            "humidity": (0, 100),
            "ph": (0, 14),
            "rainfall": (0, 3000)
        }

        for col, (min_val, max_val) in ranges.items():
            if col in df.columns:
                out_of_bounds = df[(df[col] < min_val) | (df[col] > max_val)]
                if len(out_of_bounds) > 0:
                    warnings.append(f"Column '{col}' has {len(out_of_bounds)} values outside valid range [{min_val}, {max_val}]")
            else:
                errors.append(f"Required column '{col}' missing from dataset")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "total_records_checked": len(df)
        }
