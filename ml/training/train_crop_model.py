import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler

from ml.evaluation.metrics_evaluator import evaluate_classification_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'crop_recommendation.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_select_crop_model():
    """Train candidate models, compare metrics, and persist the best model."""
    print("Loading crop recommendation dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    candidates = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }

    best_model_name = None
    best_model = None
    best_f1 = -1.0
    comparison_results = {}

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_classification_model(y_test, y_pred)
        comparison_results[name] = metrics
        print(f"Model: {name:20s} | Accuracy: {metrics['accuracy']:.4f} | F1: {metrics['f1_score']:.4f}")

        if metrics['f1_score'] > best_f1:
            best_f1 = metrics['f1_score']
            best_model_name = name
            best_model = model

    print(f"\nWinner Model: {best_model_name} with F1-Score: {best_f1:.4f}")

    # Persist artifacts
    joblib.dump(best_model, os.path.join(MODEL_DIR, 'crop_model.joblib'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'crop_scaler.joblib'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'crop_label_encoder.joblib'))
    joblib.dump(comparison_results, os.path.join(MODEL_DIR, 'crop_model_comparison.joblib'))

    print(f"Crop recommendation model successfully saved to {MODEL_DIR}")
    return comparison_results

if __name__ == '__main__':
    train_and_select_crop_model()
