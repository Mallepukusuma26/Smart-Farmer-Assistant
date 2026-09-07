import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

def get_crop_model_comparison_metrics():
    """Load and format candidate crop model evaluation metrics."""
    filepath = os.path.join(MODEL_DIR, 'crop_model_comparison.joblib')
    if os.path.exists(filepath):
        return joblib.load(filepath)
    return {}

def get_yield_model_comparison_metrics():
    """Load and format candidate yield regressor evaluation metrics."""
    filepath = os.path.join(MODEL_DIR, 'yield_model_comparison.joblib')
    if os.path.exists(filepath):
        return joblib.load(filepath)
    return {}
