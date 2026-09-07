"""
Yield Model Trainer Module for Smart Farmer Assistant.

Trains 4 machine learning regression algorithms:
1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor
4. Decision Tree Regressor

Performs feature encoding, standard scaling, model cross-validation,
evaluation (R2 Score, Mean Absolute Error, Root Mean Squared Error),
model comparison, and joblib serialization.
"""

from typing import Dict, Any, Tuple, List, Optional
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import logging

from ml.data_engineering.dataset_loader import DatasetLoader
from ml.data_engineering.dataset_cleaner import DatasetCleaner

logger = logging.getLogger(__name__)


class YieldModelTrainer:
    """
    Trains, evaluates, and persists multi-model offline crop yield regression models.
    """

    def __init__(self, data_dir: Optional[str] = None, model_dir: Optional[str] = None):
        self.data_loader = DatasetLoader(data_dir=data_dir)
        self.cleaner = DatasetCleaner()
        self.model_dir = model_dir or os.path.join(os.getcwd(), "ml", "models")
        os.makedirs(self.model_dir, exist_ok=True)

    def train_all_models(self) -> Dict[str, Any]:
        """
        Loads yield dataset, encodes crop strings, trains 4 regressor algorithms,
        evaluates R2 and RMSE, selects best model, and saves joblib artifact.
        """
        df = self.data_loader.load_yield_dataset()
        df = self.cleaner.remove_duplicates(df)

        le = LabelEncoder()
        df["crop_encoded"] = le.fit_transform(df["crop_name"].astype(str))

        feature_cols = ["crop_encoded", "rainfall_mm", "pesticides_tonnes", "avg_temp"]
        X = df[feature_cols].values
        y = df["yield_per_acre"].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        regressors = {
            "RandomForestRegressor": RandomForestRegressor(n_estimators=100, random_state=42),
            "GradientBoostingRegressor": GradientBoostingRegressor(n_estimators=100, random_state=42),
            "DecisionTreeRegressor": DecisionTreeRegressor(max_depth=8, random_state=42),
            "LinearRegression": LinearRegression()
        }

        results = {}
        best_model_name = None
        best_r2 = -999.0
        best_model_obj = None

        for name, reg in regressors.items():
            reg.fit(X_train_scaled, y_train)
            y_pred = reg.predict(X_test_scaled)

            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            cv_r2 = cross_val_score(reg, X_train_scaled, y_train, cv=5, scoring="r2")

            results[name] = {
                "r2_score": float(r2),
                "mae": float(mae),
                "rmse": float(rmse),
                "cv_mean_r2": float(np.mean(cv_r2))
            }

            logger.info(f"Yield Regressor {name}: R2={r2:.4f}, MAE={mae:.4f}, RMSE={rmse:.4f}")

            if r2 > best_r2:
                best_r2 = r2
                best_model_name = name
                best_model_obj = reg

        # Save best model and preprocessors
        model_path = os.path.join(self.model_dir, "yield_model.joblib")
        scaler_path = os.path.join(self.model_dir, "yield_scaler.joblib")
        encoder_path = os.path.join(self.model_dir, "yield_crop_encoder.joblib")
        comparison_path = os.path.join(self.model_dir, "yield_model_comparison.joblib")

        joblib.dump(best_model_obj, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(le, encoder_path)
        joblib.dump({"results": results, "best_model": best_model_name}, comparison_path)

        logger.info(f"Saved best yield model '{best_model_name}' (R2: {best_r2:.4f}) to {model_path}")

        return {
            "best_model_name": best_model_name,
            "best_r2_score": float(best_r2),
            "model_comparison": results
        }


if __name__ == "__main__":
    trainer = YieldModelTrainer()
    trainer.train_all_models()
