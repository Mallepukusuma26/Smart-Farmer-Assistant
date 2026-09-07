# Smart Farmer Assistant

**AI-Powered Crop, Soil, Fertilizer, Irrigation, Disease, Yield and Farm Profit Management System**

100% Offline-First Precision Agriculture Platform built with Python, Flask, SQLAlchemy, SQLite, Scikit-learn, Joblib, Pillow/OpenCV, and Vanilla JavaScript.

---

## Key Features

1. **Role-Based Access Control (RBAC)**: Supports 3 distinct roles: **FARMER**, **ADMIN**, and **AGRICULTURAL ADVISOR**.
2. **Soil Health Analysis**: Algorithmic scoring (0–100) based on pH, N, P, K, Organic Carbon, and Electrical Conductivity with tailored deficiency improvement plans.
3. **ML Crop Recommendation Engine**: Local Random Forest Classifier predicting top suitable crops based on soil NPK, temperature, humidity, pH, and rainfall.
4. **Fertilizer Dosage Calculator**: NPK deficit calculator returning exact dosage (kg/acre), application stages, cost estimation, and safety guidance.
5. **Irrigation Scheduling**: Evapotranspiration-based daily water requirement calculation (Liters/acre), watering frequency, next irrigation alerts, and water logs.
6. **Leaf Disease Diagnosis (Computer Vision)**: Offline image feature extraction and Random Forest classifier for instant leaf disease diagnosis and treatment plans.
7. **Crop Yield Prediction**: Regression models (Random Forest, Decision Tree, Gradient Boosting, Linear Regression) predicting harvest yield (metric tons/acre).
8. **Expense & Harvest Revenue Tracking**: Category-wise farm expense logging, harvest sale revenue tracking, and financial analytics.
9. **Profit Forecast & Break-even Calculator**: Gradient Boosting regressor computing expected revenue, net profit, profit margin %, minimum break-even yield, and break-even price per ton.
10. **Offline PDF & CSV Report Generation**: Standalone local report generation using ReportLab without external API calls.
11. **Security & Audit Trail**: Password hashing, failed login tracking, account locking, input sanitization, and security audit logs.

---

## Technology Stack

- **Backend Framework**: Python 3.11+, Flask
- **Database / ORM**: SQLite (default), SQLAlchemy ORM
- **Machine Learning**: Scikit-learn, Joblib, Pandas, NumPy, Pillow, OpenCV
- **Frontend**: HTML5, CSS3, Vanilla JS, Bootstrap, Chart.js
- **Reporting**: ReportLab (PDF), Python CSV module
- **Testing**: pytest

---

## BUILD & INSTALLATION INSTRUCTIONS

### 1. Environment & Dependency Setup
Install dependencies using standard requirements or the pinned dependency lockfile:
```bash
# Using standard requirements manifest
pip install -r requirements.txt

# Using pinned dependency lockfile (recommended for deterministic builds)
pip install -r requirements-lock.txt
```

### 2. Docker Container Build
To build and run the application container using Docker:
```bash
# Build Docker image
docker build -t smart-farmer-assistant .

# Run Docker container
docker run -p 5000:5000 smart-farmer-assistant
```

### 3. Makefile Automation
```bash
# Install dependencies
make install

# Seed database and train ML models
make setup

# Run application server
make run

# Run test suite
make test

# Run test suite with coverage report
make coverage
```

---

## 100% Offline & Zero API Key Guarantee

This application runs **entirely locally** without internet access once dependencies are installed. It does **NOT** require:
- No OpenAI API Keys
- No Gemini API Keys
- No Weather API Keys
- No Google Maps API Keys
- No paid cloud services

---

## Quick Start & Installation

### 1. Clone & Navigate
```bash
cd "Smart Farmer Assistent"
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements-lock.txt
```

### 3. Seed Database & Train Local ML Models
```bash
# Seed local database with demo accounts & catalogs
python database/seeds/seed.py

# Train local machine learning models
python ml/training/train_crop_model.py
python ml/training/train_yield_model.py
python ml/training/train_disease_model.py
python ml/training/train_profit_model.py
```

### 4. Launch Application Server
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## Demo Accounts

| Role | Username | Password |
| :--- | :--- | :--- |
| **Farmer** | `john_farmer` | `farmer123` |
| **Admin** | `admin` | `admin123` |
| **Advisor** | `advisor_smith` | `advisor123` |

---

## Running Automated Tests & Coverage

Run the complete test suite with coverage reporting:
```bash
# Run pytest test suite
pytest

# Run pytest with code coverage
pytest --cov=app --cov=ml --cov-report=term-missing
```

---

## Codebase Statistics (LOC)

To generate an accurate line count report across python, html, css, js, and documentation files:
```bash
python scripts/verify_project.py
```

---

## Technical Documentation & Architecture

Detailed technical documentation is available in the [`docs/`](./docs/) directory:
- [`ARCHITECTURE.md`](./docs/ARCHITECTURE.md)
- [`DATABASE.md`](./docs/DATABASE.md)
- [`ML_DOCUMENTATION.md`](./docs/ML_DOCUMENTATION.md)
- [`API_DOCUMENTATION.md`](./docs/API_DOCUMENTATION.md)
- [`SECURITY.md`](./docs/SECURITY.md)
