from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class MLModelRegistry(db.Model):
    """Local ML Model Registry tracking trained model versions, metrics, and persistence paths."""
    __tablename__ = 'ml_model_registry'

    id = db.Column(db.Integer, primary_key=True)
    model_key = db.Column(db.String(100), unique=True, nullable=False) # e.g. crop_recommendation_rf, yield_prediction_gbr
    display_name = db.Column(db.String(150), nullable=False)
    algorithm_type = db.Column(db.String(50), nullable=False) # Random Forest, Gradient Boosting, KNN, Decision Tree, Logistic Regression
    task_category = db.Column(db.String(50), nullable=False) # Crop Recommendation, Yield Prediction, Disease Detection, Fertilizer Recommendation, Profit Forecast
    version = db.Column(db.String(20), nullable=False, default='1.0.0')
    file_path = db.Column(db.String(255), nullable=False) # Local .joblib / .pkl file path
    scaler_file_path = db.Column(db.String(255), nullable=True)
    encoder_file_path = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    accuracy_score = db.Column(db.Float, default=0.0) # R2 score or Accuracy
    f1_score = db.Column(db.Float, default=0.0)
    mae_score = db.Column(db.Float, default=0.0) # Mean Absolute Error
    rmse_score = db.Column(db.Float, default=0.0) # Root Mean Squared Error
    training_sample_count = db.Column(db.Integer, default=0)
    hyperparameters_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    performance_logs = db.relationship('ModelPerformanceLog', backref='model', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'model_key': self.model_key,
            'display_name': self.display_name,
            'algorithm_type': self.algorithm_type,
            'task_category': self.task_category,
            'version': self.version,
            'file_path': self.file_path,
            'scaler_file_path': self.scaler_file_path,
            'encoder_file_path': self.encoder_file_path,
            'is_active': self.is_active,
            'accuracy_score': round(self.accuracy_score, 4),
            'f1_score': round(self.f1_score, 4),
            'mae_score': round(self.mae_score, 4),
            'rmse_score': round(self.rmse_score, 4),
            'training_sample_count': self.training_sample_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<MLModelRegistry key='{self.model_key}' version='{self.version}'>"


class MLDatasetMetadata(db.Model):
    """Metadata catalog for local agricultural training and evaluation datasets."""
    __tablename__ = 'ml_dataset_metadata'

    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(100), unique=True, nullable=False)
    file_path = db.Column(db.String(255), nullable=False) # Relative path to CSV file
    record_count = db.Column(db.Integer, default=0)
    column_count = db.Column(db.Integer, default=0)
    target_column = db.Column(db.String(50), nullable=False)
    feature_columns_json = db.Column(db.Text, nullable=True) # Feature column names JSON array
    data_quality_score = db.Column(db.Float, default=100.0) # 0-100%
    missing_values_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    last_validated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'dataset_name': self.dataset_name,
            'file_path': self.file_path,
            'record_count': self.record_count,
            'column_count': self.column_count,
            'target_column': self.target_column,
            'data_quality_score': round(self.data_quality_score, 1),
            'missing_values_count': self.missing_values_count,
            'duplicate_count': self.duplicate_count,
            'last_validated_at': self.last_validated_at.strftime('%Y-%m-%d %H:%M')
        }


class ModelPerformanceLog(db.Model):
    """Historical tracking of model evaluation runs and inference accuracy metrics."""
    __tablename__ = 'model_performance_logs'

    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ml_model_registry.id', ondelete='CASCADE'), nullable=False)
    evaluation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    dataset_used = db.Column(db.String(100), nullable=False)
    test_accuracy = db.Column(db.Float, nullable=False)
    precision_score = db.Column(db.Float, default=0.0)
    recall_score = db.Column(db.Float, default=0.0)
    f1_score = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'model_id': self.model_id,
            'evaluation_date': self.evaluation_date.strftime('%Y-%m-%d %H:%M'),
            'dataset_used': self.dataset_used,
            'test_accuracy': round(self.test_accuracy, 4),
            'precision_score': round(self.precision_score, 4),
            'recall_score': round(self.recall_score, 4),
            'f1_score': round(self.f1_score, 4),
            'notes': self.notes
        }
