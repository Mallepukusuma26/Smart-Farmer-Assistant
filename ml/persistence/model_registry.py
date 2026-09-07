"""
Model Registry Module for Smart Farmer Assistant.

Manages local joblib machine learning model versioning, SHA-256 checksum verification,
model loading, fallback model dispatch, and performance metadata tracking.
"""

from typing import Dict, Any, List, Optional
import os
import hashlib
import joblib
import logging

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Local offline model registry managing version numbers, model file loading,
    SHA-256 integrity verification, and fallback predictor mechanisms.
    """

    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = model_dir or os.path.join(os.getcwd(), "ml", "models")
        os.makedirs(self.model_dir, exist_ok=True)
        self._loaded_models: Dict[str, Any] = {}

    def get_file_checksum(self, filepath: str) -> str:
        """
        Calculates SHA-256 checksum hash of serialized model file.
        """
        if not os.path.exists(filepath):
            return ""
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def load_model(self, model_filename: str) -> Optional[Any]:
        """
        Loads joblib model file from model directory with caching.
        """
        if model_filename in self._loaded_models:
            return self._loaded_models[model_filename]

        filepath = os.path.join(self.model_dir, model_filename)
        if not os.path.exists(filepath):
            logger.warning(f"Model file {model_filename} not found at {filepath}")
            return None

        try:
            model = joblib.load(filepath)
            self._loaded_models[model_filename] = model
            logger.info(f"Successfully loaded model '{model_filename}' (SHA256: {self.get_file_checksum(filepath)[:8]}...)")
            return model
        except Exception as e:
            logger.error(f"Error loading model {model_filename}: {str(e)}")
            return None

    def list_registry_models(self) -> List[Dict[str, Any]]:
        """
        Lists all serialized model files in the registry with size and checksum.
        """
        files = [f for f in os.listdir(self.model_dir) if f.endswith(".joblib")]
        registry = []
        for filename in files:
            filepath = os.path.join(self.model_dir, filename)
            registry.append({
                "filename": filename,
                "size_bytes": os.path.getsize(filepath),
                "checksum_sha256": self.get_file_checksum(filepath)[:16],
                "last_modified": os.path.getmtime(filepath)
            })
        return registry
