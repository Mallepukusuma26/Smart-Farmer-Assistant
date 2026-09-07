"""
Dataset Cleaner Module for Smart Farmer Assistant.

Provides data cleaning pipelines: missing value imputation (mean/median/mode),
outlier detection and filtering via Interquartile Range (IQR) and Z-score methods,
duplicate row removal, and range validation.
"""

from typing import Dict, Any, List, Tuple, Optional, Union
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DatasetCleaner:
    """
    Cleaner module handling numerical and categorical data preprocessing,
    missing value handling, outlier clipping, and duplicate removal.
    """

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes exact duplicate rows from DataFrame.
        """
        initial_count = len(df)
        cleaned_df = df.drop_duplicates().reset_index(drop=True)
        dropped_count = initial_count - len(cleaned_df)
        if dropped_count > 0:
            logger.info(f"Removed {dropped_count} duplicate rows")
        return cleaned_df

    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame,
        strategy: str = "median",
        fill_values: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Imputes missing values using mean, median, mode, or custom fill values.
        """
        cleaned_df = df.copy()
        if fill_values:
            return cleaned_df.fillna(value=fill_values)

        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        categorical_cols = cleaned_df.select_dtypes(exclude=[np.number]).columns

        for col in numeric_cols:
            if cleaned_df[col].isnull().sum() > 0:
                if strategy == "mean":
                    fill_val = cleaned_df[col].mean()
                elif strategy == "median":
                    fill_val = cleaned_df[col].median()
                else:
                    fill_val = 0
                cleaned_df[col] = cleaned_df[col].fillna(fill_val)

        for col in categorical_cols:
            if cleaned_df[col].isnull().sum() > 0:
                mode_val = cleaned_df[col].mode()
                fill_val = mode_val[0] if not mode_val.empty else "Unknown"
                cleaned_df[col] = cleaned_df[col].fillna(fill_val)

        return cleaned_df

    @staticmethod
    def remove_outliers_iqr(
        df: pd.DataFrame,
        columns: List[str],
        factor: float = 1.5
    ) -> pd.DataFrame:
        """
        Filters out rows with numerical values outside Q1 - factor*IQR or Q3 + factor*IQR.
        """
        cleaned_df = df.copy()
        for col in columns:
            if col in cleaned_df.columns:
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - factor * IQR
                upper_bound = Q3 + factor * IQR
                cleaned_df = cleaned_df[(cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)]

        return cleaned_df.reset_index(drop=True)

    @staticmethod
    def clip_outliers_zscore(
        df: pd.DataFrame,
        columns: List[str],
        threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Clips extreme numerical values exceeding threshold standard deviations from mean.
        """
        cleaned_df = df.copy()
        for col in columns:
            if col in cleaned_df.columns and pd.api.types.is_numeric_dtype(cleaned_df[col]):
                mean = cleaned_df[col].mean()
                std = cleaned_df[col].std()
                if std > 0:
                    lower_limit = mean - threshold * std
                    upper_limit = mean + threshold * std
                    cleaned_df[col] = np.clip(cleaned_df[col], lower_limit, upper_limit)

        return cleaned_df
