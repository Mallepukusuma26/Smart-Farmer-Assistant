"""
Dataset Loader Module for Smart Farmer Assistant.

Handles loading, validating, and parsing local CSV datasets for Crop Recommendation,
Crop Yield Regression, Plant Disease Features, Fertilizer Requirements, and Farm Profitability.
Supports schema column mapping and normalization.
"""

from typing import Dict, Any, List, Tuple, Optional
import os
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Local offline dataset loader providing dataset parsing, schema mapping,
    column alias normalization, and baseline statistical summaries.
    """

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or os.path.join(os.getcwd(), "ml", "datasets")
        os.makedirs(self.data_dir, exist_ok=True)

    def load_crop_dataset(self) -> pd.DataFrame:
        """
        Loads local crop recommendation dataset (N, P, K, temperature, humidity, ph, rainfall, label).
        """
        filepath = os.path.join(self.data_dir, "crop_recommendation.csv")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Crop dataset not found at {filepath}")

        df = pd.read_csv(filepath)
        return df

    def load_yield_dataset(self) -> pd.DataFrame:
        """
        Loads local crop yield regression dataset. Normalizes column headers if needed.
        """
        filepath = os.path.join(self.data_dir, "yield_prediction.csv")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Yield dataset not found at {filepath}")

        df = pd.read_csv(filepath)

        # Standardize column names
        rename_map = {
            "crop": "crop_name",
            "rainfall": "rainfall_mm",
            "yield_tons": "yield_per_acre"
        }
        df = df.rename(columns=rename_map)

        if "pesticides_tonnes" not in df.columns:
            df["pesticides_tonnes"] = 0.5
        if "avg_temp" not in df.columns and "temperature" in df.columns:
            df["avg_temp"] = df["temperature"]

        return df

    def load_disease_features_dataset(self) -> pd.DataFrame:
        """
        Loads local plant leaf disease extracted computer vision features dataset.
        """
        filepath = os.path.join(self.data_dir, "disease_features.csv")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Disease features dataset not found at {filepath}")

        df = pd.read_csv(filepath)
        if "disease" in df.columns and "disease_label" not in df.columns:
            df = df.rename(columns={"disease": "disease_label"})
        return df

    def load_profit_dataset(self) -> pd.DataFrame:
        """
        Loads local farm profitability history dataset.
        """
        filepath = os.path.join(self.data_dir, "profit_history.csv")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Profit dataset not found at {filepath}")

        df = pd.read_csv(filepath)
        rename_map = {
            "crop": "crop_name",
            "area_acres": "land_area_acres",
            "estimated_expenses": "total_investment",
            "yield_tons": "expected_yield_per_acre",
            "selling_price_per_ton": "market_price",
            "expected_profit": "net_profit"
        }
        df = df.rename(columns=rename_map)
        return df
