# Smart Farmer Assistant — Developer Guide

## Development Environment Setup

1. Requirements: Python 3.11+, pip, virtual environment (optional).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database seed & train local ML models:
   ```bash
   python database/seeds/seed.py
   python -c "from ml.training.train_crop_model import train_and_select_crop_model; train_and_select_crop_model()"
   python -c "from ml.training.train_yield_model import train_and_select_yield_model; train_and_select_yield_model()"
   python -c "from ml.training.train_disease_model import train_disease_model; train_disease_model()"
   python -c "from ml.training.train_profit_model import train_profit_model; train_profit_model()"
   ```
4. Run development server:
   ```bash
   python run.py
   ```

## Adding New Features

- **New Database Entity**: Create entity class in `app/models/`, export in `app/models/__init__.py`, and register in `database/seeds/seed.py`.
- **New Service**: Add business logic class in `app/services/` and export in `app/services/__init__.py`.
- **New Route**: Add route handler in appropriate blueprint in `app/routes/`.
- **New ML Model**: Add training script in `ml/training/` and prediction service in `ml/prediction/`.
