"""
Disease Model Trainer Module for Smart Farmer Assistant.

Trains computer vision disease classifier on features extracted from plant leaf images
(color RGB/HSV statistics, GLCM texture contrast/energy, Sobel edge response, Hu shape moments).
"""

from typing import Dict, Any, Tuple, List, Optional
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import logging

from ml.data_engineering.dataset_loader import DatasetLoader

logger = logging.getLogger(__name__)


class DiseaseModelTrainer:
    """
    Trains and persists plant leaf disease classifier on computer vision feature descriptors.
    """

    def __init__(self, data_dir: Optional[str] = None, model_dir: Optional[str] = None):
        self.data_loader = DatasetLoader(data_dir=data_dir)
        self.model_dir = model_dir or os.path.join(os.getcwd(), "ml", "models")
        os.makedirs(self.model_dir, exist_ok=True)

    def train_disease_classifier(self) -> Dict[str, Any]:
        """
        Loads extracted feature matrix dataset, trains RandomForest classifier,
        evaluates precision/recall/F1, and serializes classifier model to joblib.
        """
        df = self.data_loader.load_disease_features_dataset()

        feature_cols = [c for c in df.columns if c != "disease_label"]
        X = df[feature_cols].values
        y_raw = df["disease_label"].values

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train_scaled, y_train)

        y_pred = clf.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        # Save artifacts
        model_path = os.path.join(self.model_dir, "disease_model.joblib")
        scaler_path = os.path.join(self.model_dir, "disease_scaler.joblib")
        encoder_path = os.path.join(self.model_dir, "disease_label_encoder.joblib")

        joblib.dump(clf, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(label_encoder, encoder_path)

        logger.info(f"Saved disease classification model (Accuracy: {acc:.4f}, F1: {f1:.4f}) to {model_path}")

        return {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "num_features": len(feature_cols),
            "disease_classes": list(label_encoder.classes_)
        }


if __name__ == "__main__":
    trainer = DiseaseModelTrainer()
    trainer.train_disease_classifier()
