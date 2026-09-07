import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.training.train_crop_model import train_and_select_crop_model
from ml.training.train_yield_model import train_and_select_yield_model
from ml.training.train_disease_model import train_disease_model
from ml.training.train_profit_model import train_profit_model

if __name__ == '__main__':
    print("=== Retraining Local Machine Learning Models ===")
    train_and_select_crop_model()
    train_and_select_yield_model()
    train_disease_model()
    train_profit_model()
    print("=== All Models Retrained and Saved Successfully ===")
