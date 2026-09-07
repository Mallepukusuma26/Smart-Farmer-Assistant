# Smart Farmer Assistant — Architecture Specification

## Overview

Smart Farmer Assistant is engineered with a modular, 3-tier offline-first architecture separating presentation, application business logic, and local machine learning inference.

```
┌────────────────────────────────────────────────────────┐
│               PRESENTATION LAYER (UI)                  │
│   Jinja2 HTML Templates | Bootstrap 5 | Chart.js JS     │
└───────────────────────────┬────────────────────────────┘
                            │ (HTTP / Form / AJAX)
┌───────────────────────────▼────────────────────────────┐
│              APPLICATION & CONTROLLER LAYER            │
│   Flask Blueprints | RBAC Decorators | Audit Middleware │
└───────────────────────────┬────────────────────────────┘
                            │ (Service Calls)
┌───────────────────────────▼────────────────────────────┐
│                  SERVICE & DOMAIN LAYER                │
│  AuthService | FarmService | SoilService | CropService │
│  FertilizerService | IrrigationService | YieldService  │
│  DiseaseService | FinanceService | ReportService       │
└─────────────┬──────────────────────────────┬───────────┘
              │                              │
┌─────────────▼──────────┐      ┌────────────▼───────────┐
│     DATABASE LAYER     │      │   LOCAL ML PIPELINE    │
│  SQLAlchemy ORM        │      │   Scikit-Learn Joblib  │
│  SQLite Database       │      │   Pillow / OpenCV CV   │
└────────────────────────┘      └────────────────────────┘
```

## Core Architectural Layers

1. **Routes & Controllers (`app/routes/`)**: Handles request routing, session validation, form parsing, and response rendering.
2. **Services (`app/services/`)**: Implements application business logic, coordinate models, algorithms, and local ML predictors.
3. **Database Models (`app/models/`)**: Normalized SQLAlchemy ORM models enforcing foreign keys, constraints, and relationships.
4. **Machine Learning Pipeline (`ml/`)**: 100% offline data preprocessing, feature engineering, model training, evaluation, persistent joblib models, and prediction services.
5. **Report Generation (`app/utils/`)**: Standalone PDF rendering using ReportLab and CSV generation.
