"""
Profit Model Trainer Module for Smart Farmer Assistant.

Trains farm profitability regressor model on financial investment parameters,
land acreage, crop expected yield, and market commodity prices.
"""

from typing import Dict, Any, Tuple, List, Optional
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import logging

from ml.data_engineering.dataset_loader import DatasetLoader

logger = logging.getLogger(__name__)


class ProfitModelTrainer:
    """
    Trains and persists farm profitability regressor model.
    """

    def __init__(self, data_dir: Optional[str] = None, model_dir: Optional[str] = None):
        self.data_loader = DatasetLoader(data_dir=data_dir)
        self.model_dir = model_dir or os.path.join(os.getcwd(), "ml", "models")
        os.makedirs(self.model_dir, exist_ok=True)

    def train_profit_model(self) -> Dict[str, Any]:
        """
        Loads profit history dataset, trains RandomForestRegressor, evaluates R2, and saves joblib model.
        """
        df = self.data_loader.load_profit_dataset()

        le = LabelEncoder()
        df["crop_encoded"] = le.fit_transform(df["crop_name"].astype(str))

        feature_cols = ["crop_encoded", "total_investment", "land_area_acres", "expected_yield_per_acre", "market_price"]
        X = df[feature_cols].values
        y = df["net_profit"].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        reg = RandomForestRegressor(n_estimators=100, random_state=42)
        reg.fit(X_train_scaled, y_train)

        y_pred = reg.predict(X_test_scaled)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Save artifacts
        model_path = os.path.join(self.model_dir, "profit_model.joblib")
        scaler_path = os.path.join(self.model_dir, "profit_scaler.joblib")
        encoder_path = os.path.join(self.model_dir, "profit_crop_encoder.joblib")

        joblib.dump(reg, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(le, encoder_path)

        logger.info(f"Saved profit model (R2 Score: {r2:.4f}, MAE: {mae:.2f}) to {model_path}")

        return {
            "r2_score": float(r2),
            "mae": float(mae),
            "rmse": float(rmse)
        }


if __name__ == "__main__":
    trainer = ProfitModelTrainer()
    trainer.train_profit_model()
