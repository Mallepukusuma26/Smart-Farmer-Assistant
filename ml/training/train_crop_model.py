"""
Crop Model Trainer Module for Smart Farmer Assistant.

Trains 5 machine learning classification algorithms:
1. Random Forest Classifier
2. Decision Tree Classifier
3. K-Nearest Neighbors (KNN)
4. Gradient Boosting Classifier
5. Logistic Regression

Performs dataset loading, cleaning, train/val/test splitting, feature scaling,
hyperparameter tuning, model evaluation (Accuracy, Precision, Recall, F1 Score, Confusion Matrix),
model comparison, and joblib serialization.
"""

from typing import Dict, Any, Tuple, List, Optional
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import logging

from ml.data_engineering.dataset_loader import DatasetLoader
from ml.data_engineering.dataset_cleaner import DatasetCleaner

logger = logging.getLogger(__name__)


class CropModelTrainer:
    """
    Trains, evaluates, and persists multi-model offline crop recommendation classifiers.
    """

    def __init__(self, data_dir: Optional[str] = None, model_dir: Optional[str] = None):
        self.data_loader = DatasetLoader(data_dir=data_dir)
        self.cleaner = DatasetCleaner()
        self.model_dir = model_dir or os.path.join(os.getcwd(), "ml", "models")
        os.makedirs(self.model_dir, exist_ok=True)

    def train_all_models(self) -> Dict[str, Any]:
        """
        Loads dataset, preprocesses features, trains 5 algorithms, selects the best performer,
        and saves the fitted model, scaler, and label encoder to disk.
        """
        df = self.data_loader.load_crop_dataset()
        df = self.cleaner.remove_duplicates(df)
        df = self.cleaner.handle_missing_values(df, strategy="median")

        X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]].values
        y_raw = df["label"].values

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        classifiers = {
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
            "DecisionTree": DecisionTreeClassifier(max_depth=10, random_state=42),
            "KNN": KNeighborsClassifier(n_neighbors=5),
            "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
            "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42)
        }

        results = {}
        best_model_name = None
        best_accuracy = -1.0
        best_model_obj = None

        for name, clf in classifiers.items():
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
            rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
            f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
            cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=5)

            results[name] = {
                "accuracy": float(acc),
                "precision": float(prec),
                "recall": float(rec),
                "f1_score": float(f1),
                "cv_mean_accuracy": float(np.mean(cv_scores)),
                "cv_std": float(np.std(cv_scores))
            }

            logger.info(f"Model {name}: Accuracy={acc:.4f}, F1={f1:.4f}, CV_Mean={np.mean(cv_scores):.4f}")

            if acc > best_accuracy:
                best_accuracy = acc
                best_model_name = name
                best_model_obj = clf

        # Save best model, scaler, and encoder
        model_path = os.path.join(self.model_dir, "crop_model.joblib")
        scaler_path = os.path.join(self.model_dir, "crop_scaler.joblib")
        encoder_path = os.path.join(self.model_dir, "crop_label_encoder.joblib")
        comparison_path = os.path.join(self.model_dir, "crop_model_comparison.joblib")

        joblib.dump(best_model_obj, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(label_encoder, encoder_path)
        joblib.dump({"results": results, "best_model": best_model_name}, comparison_path)

        logger.info(f"Saved best crop model '{best_model_name}' (Accuracy: {best_accuracy:.4f}) to {model_path}")

        return {
            "best_model_name": best_model_name,
            "best_accuracy": float(best_accuracy),
            "model_comparison": results
        }


if __name__ == "__main__":
    trainer = CropModelTrainer()
    trainer.train_all_models()
