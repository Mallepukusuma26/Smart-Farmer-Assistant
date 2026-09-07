from typing import Optional, List, Dict, Any, Tuple
import json
from datetime import datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.ml_metadata import MLModelRegistry, MLDatasetMetadata, ModelPerformanceLog
from app.repositories.base_repository import BaseRepository

class MLMetadataRepository(BaseRepository[MLModelRegistry]):
    """Data Access Repository for Local Machine Learning Model Registry and Dataset Catalogs."""

    def __init__(self):
        super().__init__(MLModelRegistry)

    def find_by_key(self, model_key: str) -> Optional[MLModelRegistry]:
        """Look up ML model registry entry by key."""
        return db.session.query(MLModelRegistry).filter_by(model_key=model_key).first()

    def register_model(self, model_key: str, display_name: str, algorithm_type: str, task_category: str, file_path: str, version: str = '1.0.0', accuracy_score: float = 0.0, f1_score: float = 0.0, mae_score: float = 0.0, rmse_score: float = 0.0, training_sample_count: int = 0, scaler_path: Optional[str] = None, encoder_path: Optional[str] = None, hyperparameters: Optional[Dict[str, Any]] = None) -> MLModelRegistry:
        """Register or update trained ML model version metadata."""
        params_str = json.dumps(hyperparameters) if hyperparameters else None
        model = self.find_by_key(model_key)
        if not model:
            model = MLModelRegistry(
                model_key=model_key,
                display_name=display_name,
                algorithm_type=algorithm_type,
                task_category=task_category,
                version=version,
                file_path=file_path,
                scaler_file_path=scaler_path,
                encoder_file_path=encoder_path,
                accuracy_score=accuracy_score,
                f1_score=f1_score,
                mae_score=mae_score,
                rmse_score=rmse_score,
                training_sample_count=training_sample_count,
                hyperparameters_json=params_str,
                is_active=True
            )
            db.session.add(model)
        else:
            model.display_name = display_name
            model.algorithm_type = algorithm_type
            model.task_category = task_category
            model.version = version
            model.file_path = file_path
            model.scaler_file_path = scaler_path
            model.encoder_file_path = encoder_path
            model.accuracy_score = accuracy_score
            model.f1_score = f1_score
            model.mae_score = mae_score
            model.rmse_score = rmse_score
            model.training_sample_count = training_sample_count
            if params_str:
                model.hyperparameters_json = params_str
            model.updated_at = datetime.utcnow()
        db.session.commit()
        return model

    def get_active_models_by_category(self, task_category: str) -> List[MLModelRegistry]:
        """Fetch active trained models for a specific ML task."""
        return db.session.query(MLModelRegistry).filter_by(task_category=task_category, is_active=True).all()

    def register_dataset(self, dataset_name: str, file_path: str, record_count: int, column_count: int, target_column: str, feature_columns: List[str], data_quality_score: float = 100.0, missing_count: int = 0, duplicate_count: int = 0) -> MLDatasetMetadata:
        """Register dataset metadata in local metadata store."""
        ds = db.session.query(MLDatasetMetadata).filter_by(dataset_name=dataset_name).first()
        feat_json = json.dumps(feature_columns)
        if not ds:
            ds = MLDatasetMetadata(
                dataset_name=dataset_name,
                file_path=file_path,
                record_count=record_count,
                column_count=column_count,
                target_column=target_column,
                feature_columns_json=feat_json,
                data_quality_score=data_quality_score,
                missing_values_count=missing_count,
                duplicate_count=duplicate_count
            )
            db.session.add(ds)
        else:
            ds.file_path = file_path
            ds.record_count = record_count
            ds.column_count = column_count
            ds.target_column = target_column
            ds.feature_columns_json = feat_json
            ds.data_quality_score = data_quality_score
            ds.missing_values_count = missing_count
            ds.duplicate_count = duplicate_count
            ds.last_validated_at = datetime.utcnow()
        db.session.commit()
        return ds

    def log_evaluation_run(self, model_id: int, dataset_used: str, test_accuracy: float, precision_score: float = 0.0, recall_score: float = 0.0, f1_score: float = 0.0, notes: Optional[str] = None) -> ModelPerformanceLog:
        """Record model evaluation benchmark results."""
        perf = ModelPerformanceLog(
            model_id=model_id,
            dataset_used=dataset_used,
            test_accuracy=test_accuracy,
            precision_score=precision_score,
            recall_score=recall_score,
            f1_score=f1_score,
            notes=notes
        )
        db.session.add(perf)
        db.session.commit()
        return perf
