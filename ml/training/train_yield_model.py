import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from ml.evaluation.metrics_evaluator import evaluate_regression_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'yield_prediction.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_select_yield_model():
    """Train regression candidate models for crop yield prediction."""
    print("Loading crop yield dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=['yield_tons'])
    y = df['yield_tons']

    categorical_features = ['crop', 'soil_type']
    numerical_features = ['area_acres', 'nitrogen', 'phosphorus', 'potassium', 'ph', 'temperature', 'rainfall', 'irrigation_liters', 'fertilizer_kg']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    candidates = {
        'Linear Regression': LinearRegression(),
        'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42)
    }

    best_model_name = None
    best_pipeline = None
    best_r2 = -float('inf')
    comparison_results = {}

    for name, model in candidates.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        metrics = evaluate_regression_model(y_test, y_pred)
        comparison_results[name] = metrics
        print(f"Regressor: {name:30s} | R2: {metrics['r2_score']:.4f} | RMSE: {metrics['rmse']:.4f}")

        if metrics['r2_score'] > best_r2:
            best_r2 = metrics['r2_score']
            best_model_name = name
            best_pipeline = pipeline

    print(f"\nWinner Regressor: {best_model_name} with R2 Score: {best_r2:.4f}")

    joblib.dump(best_pipeline, os.path.join(MODEL_DIR, 'yield_model.joblib'))
    joblib.dump(comparison_results, os.path.join(MODEL_DIR, 'yield_model_comparison.joblib'))

    print(f"Yield prediction model saved to {MODEL_DIR}")
    return comparison_results

if __name__ == '__main__':
    train_and_select_yield_model()
