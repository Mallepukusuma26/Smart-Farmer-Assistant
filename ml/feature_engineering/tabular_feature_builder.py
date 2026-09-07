"""
Tabular Feature Builder Module for Smart Farmer Assistant.

Engineers domain-specific agricultural tabular features:
NPK ratios, temperature-humidity index (THI), rainfall deficit metrics, and soil buffer factors.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class TabularFeatureBuilder:
    """
    Computes domain-engineered features for tabular ML models.
    """

    @staticmethod
    def build_crop_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates N:P ratio, N:K ratio, P:K ratio, and Temperature-Humidity Index (THI) columns.
        """
        data = df.copy()

        # NPK Nutrient Ratios
        data["np_ratio"] = np.where(data["P"] > 0, data["N"] / data["P"], data["N"])
        data["nk_ratio"] = np.where(data["K"] > 0, data["N"] / data["K"], data["N"])
        data["pk_ratio"] = np.where(data["K"] > 0, data["P"] / data["K"], data["P"])

        # Temperature Humidity Index (THI = T - (0.55 - 0.55*RH/100)*(T - 58))
        # Using Celsius THI formula: T - ((0.55 - 0.0055*RH)*(T - 14.5))
        data["thi_index"] = data["temperature"] - ((0.55 - 0.0055 * data["humidity"]) * (data["temperature"] - 14.5))

        return data
