import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
)

def evaluate_classification_model(y_true, y_pred):
    """Compute classification metrics: Accuracy, Precision, Recall, F1 Score, Confusion Matrix."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred).tolist()

    return {
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'f1_score': round(float(f1), 4),
        'confusion_matrix': cm
    }

def evaluate_regression_model(y_true, y_pred):
    """Compute regression metrics: MAE, MSE, RMSE, R2 Score."""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    return {
        'mae': round(float(mae), 4),
        'mse': round(float(mse), 4),
        'rmse': round(float(rmse), 4),
        'r2_score': round(float(r2), 4)
    }
