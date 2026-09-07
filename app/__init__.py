import os
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from config import config_by_name
from app.extensions import db, login_manager
from app.models.user import User
from app.middleware.error_middleware import register_error_handlers
from app.routes import auth_bp, farmer_bp, admin_bp, advisor_bp, report_bp, api_bp

def create_app(config_name='development'):
    """Application factory for Smart Farmer Assistant."""
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )

    # Load configuration
    config_obj = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_obj)

    # Create storage directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['ML_MODEL_DIR'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(farmer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(advisor_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(api_bp)

    # Register Error Handlers
    register_error_handlers(app)

    # Root landing page route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif current_user.is_advisor():
                return redirect(url_for('advisor.dashboard'))
            return redirect(url_for('farmer.dashboard'))
        return render_template('landing.html')

    return app
