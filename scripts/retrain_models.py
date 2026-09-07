"""
Script to retrain and update all offline machine learning models for Smart Farmer Assistant.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.training.train_crop_model import CropModelTrainer
from ml.training.train_yield_model import YieldModelTrainer
from ml.training.train_disease_model import DiseaseModelTrainer
from ml.training.train_profit_model import ProfitModelTrainer


def retrain_all_models():
    print("=== Retraining Local Machine Learning Models ===")

    print("1. Training Crop Recommendation Classifier Models...")
    crop_trainer = CropModelTrainer()
    crop_res = crop_trainer.train_all_models()
    print(f"   -> Best Model: {crop_res['best_model_name']} (Accuracy: {crop_res['best_accuracy']:.4f})")

    print("2. Training Crop Yield Regressor Models...")
    yield_trainer = YieldModelTrainer()
    yield_res = yield_trainer.train_all_models()
    print(f"   -> Best Model: {yield_res['best_model_name']} (R2 Score: {yield_res['best_r2_score']:.4f})")

    print("3. Training Plant Disease Computer Vision Classifier...")
    disease_trainer = DiseaseModelTrainer()
    disease_res = disease_trainer.train_disease_classifier()
    print(f"   -> Disease Model Accuracy: {disease_res['accuracy']:.4f}")

    print("4. Training Farm Profitability Predictor Model...")
    profit_trainer = ProfitModelTrainer()
    profit_res = profit_trainer.train_profit_model()
    print(f"   -> Profit Model R2 Score: {profit_res['r2_score']:.4f}")

    print("=== All 4 Local Machine Learning Models Retrained and Serialized Successfully ===")


if __name__ == "__main__":
    retrain_all_models()
