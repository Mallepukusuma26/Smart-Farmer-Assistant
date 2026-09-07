import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from ml.evaluation.metrics_evaluator import evaluate_regression_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'profit_history.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_profit_model():
    """Train Gradient Boosting regressor for farm profit prediction."""
    print("Loading profit history dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df[['crop', 'area_acres', 'yield_tons', 'selling_price_per_ton', 'estimated_expenses', 'expected_revenue']]
    y = df['expected_profit']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['area_acres', 'yield_tons', 'selling_price_per_ton', 'estimated_expenses', 'expected_revenue']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['crop'])
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', GradientBoostingRegressor(random_state=42))])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metrics = evaluate_regression_model(y_test, y_pred)
    print(f"Profit Model R2 Score: {metrics['r2_score']:.4f} | RMSE: {metrics['rmse']:.4f}")

    joblib.dump(pipeline, os.path.join(MODEL_DIR, 'profit_model.joblib'))
    print(f"Profit prediction model saved to {MODEL_DIR}")
    return metrics

if __name__ == '__main__':
    train_profit_model()
