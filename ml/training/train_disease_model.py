import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

from ml.evaluation.metrics_evaluator import evaluate_classification_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'disease_features.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_disease_model():
    """Train Random Forest classifier for offline leaf disease detection."""
    print("Loading disease feature dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df[['mean_hue', 'mean_saturation', 'mean_value', 'lesion_ratio', 'texture_contrast']]
    y = df['disease']

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = evaluate_classification_model(y_test, y_pred)
    print(f"Disease Model Accuracy: {metrics['accuracy']:.4f} | F1: {metrics['f1_score']:.4f}")

    joblib.dump(model, os.path.join(MODEL_DIR, 'disease_model.joblib'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'disease_scaler.joblib'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'disease_label_encoder.joblib'))

    print(f"Disease classifier model saved to {MODEL_DIR}")
    return metrics

if __name__ == '__main__':
    train_disease_model()
