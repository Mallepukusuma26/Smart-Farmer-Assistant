from app.routes.auth_routes import auth_bp
from app.routes.farmer_routes import farmer_bp
from app.routes.admin_routes import admin_bp
from app.routes.advisor_routes import advisor_bp
from app.routes.report_routes import report_bp
from app.routes.api_routes import api_bp

__all__ = ['auth_bp', 'farmer_bp', 'admin_bp', 'advisor_bp', 'report_bp', 'api_bp']
