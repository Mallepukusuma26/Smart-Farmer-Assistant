import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base Configuration Class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smart-farmer-assistant-secret-key-production-offline-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads & Reports Directories
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    REPORT_FOLDER = os.path.join(BASE_DIR, 'reports')
    ML_MODEL_DIR = os.path.join(BASE_DIR, 'ml', 'models')
    ML_DATASET_DIR = os.path.join(BASE_DIR, 'ml', 'datasets')
    
    # Security Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file upload size
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
    
    # Default pagination
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Development Configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'smart_farmer_dev.db')}"


class TestingConfig(Config):
    """Testing Configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'smart_farmer_prod.db')}"


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
