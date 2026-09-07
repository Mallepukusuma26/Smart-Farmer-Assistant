"""
Feature Transformer Module for Smart Farmer Assistant.

Provides custom scikit-learn compatible feature transformations: Standard Scaling,
MinMax Scaling, Label Encoding, One-Hot Encoding, and Polynomial Feature Generation.
"""

from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder, PolynomialFeatures
import joblib
import logging

logger = logging.getLogger(__name__)


class FeatureTransformer:
    """
    Handles numerical feature normalization, scaling, categorical encoding,
    and polynomial feature creation with model persistence capabilities.
    """

    def __init__(self, scaler_type: str = "standard"):
        self.scaler_type = scaler_type
        if scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            self.scaler = StandardScaler()

        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.onehot_encoder: Optional[OneHotEncoder] = None
        self.poly: Optional[PolynomialFeatures] = None
        self.fitted = False

    def fit_transform_numeric(
        self,
        df: pd.DataFrame,
        numeric_columns: List[str]
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Fits scaler on numerical columns and returns scaled numpy array along with parameters.
        """
        data = df[numeric_columns].values
        scaled_data = self.scaler.fit_transform(data)
        self.fitted = True

        params = {
            "mean": getattr(self.scaler, "mean_", None),
            "scale": getattr(self.scaler, "scale_", None),
            "min": getattr(self.scaler, "data_min_", None),
            "max": getattr(self.scaler, "data_max_", None)
        }
        return scaled_data, params

    def transform_numeric(
        self,
        df: pd.DataFrame,
        numeric_columns: List[str]
    ) -> np.ndarray:
        """
        Transforms numerical columns using fitted scaler.
        """
        if not self.fitted:
            raise RuntimeError("Transformer must be fitted before calling transform")
        return self.scaler.transform(df[numeric_columns].values)

    def encode_categorical(
        self,
        df: pd.DataFrame,
        categorical_columns: List[str]
    ) -> pd.DataFrame:
        """
        Fits label encoders on categorical columns and replaces values with encoded integers.
        """
        encoded_df = df.copy()
        for col in categorical_columns:
            if col in encoded_df.columns:
                le = LabelEncoder()
                encoded_df[col] = le.fit_transform(encoded_df[col].astype(str))
                self.label_encoders[col] = le
        return encoded_df

    def inverse_transform_label(self, column_name: str, encoded_values: Union[List[int], np.ndarray]) -> List[str]:
        """
        Decodes integer label encodings back to string class names.
        """
        if column_name not in self.label_encoders:
            raise KeyError(f"No label encoder found for column '{column_name}'")
        return list(self.label_encoders[column_name].inverse_transform(encoded_values))

    def save(self, filepath: str) -> None:
        """
        Saves transformer state and fitted scalers to file via joblib.
        """
        state = {
            "scaler_type": self.scaler_type,
            "scaler": self.scaler,
            "label_encoders": self.label_encoders,
            "fitted": self.fitted
        }
        joblib.dump(state, filepath)
        logger.info(f"FeatureTransformer saved to {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "FeatureTransformer":
        """
        Loads fitted FeatureTransformer instance from file.
        """
        state = joblib.load(filepath)
        instance = cls(scaler_type=state["scaler_type"])
        instance.scaler = state["scaler"]
        instance.label_encoders = state["label_encoders"]
        instance.fitted = state["fitted"]
        return instance
