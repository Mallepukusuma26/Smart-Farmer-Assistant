# Smart Farmer Assistant — Machine Learning Documentation

## Local Machine Learning Models Overview

All ML models in Smart Farmer Assistant operate 100% offline using locally stored binary models saved in `ml/models/`.

### 1. Crop Recommendation Model
- **Task**: Multi-class Classification (22 Crop Types)
- **Candidate Models Evaluated**: Decision Tree, Random Forest Classifier, KNN, Logistic Regression
- **Selected Model**: **Random Forest Classifier**
- **Validation Metrics**: F1-Score = 0.9977, Accuracy = 99.77%
- **Input Features**: `[N, P, K, temperature, humidity, ph, rainfall]`

### 2. Crop Yield Regressor
- **Task**: Multi-variable Yield Regression (Metric Tons / Acre)
- **Candidate Models Evaluated**: Linear Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor
- **Selected Model**: **Random Forest Regressor**
- **Validation Metrics**: $R^2$ Score = 0.9830, RMSE = 9.90
- **Input Features**: `[crop, soil_type, area_acres, nitrogen, phosphorus, potassium, ph, temperature, rainfall, irrigation_liters, fertilizer_kg]`

### 3. Leaf Disease Computer Vision Classifier
- **Task**: Image Feature Extraction & Multi-class Leaf Disease Classification
- **Feature Extraction**: HSV Color space mean values, Lesion Ratio Masking, and Texture Contrast StDev via Pillow & NumPy.
- **Model**: **Random Forest Classifier**

### 4. Farm Profit Forecasting Regressor
- **Task**: Net Profit & Break-even Regression
- **Selected Model**: **Gradient Boosting Regressor**
- **Validation Metrics**: $R^2$ Score = 0.9988
- **Input Features**: `[crop, area_acres, yield_tons, selling_price_per_ton, estimated_expenses, expected_revenue]`
