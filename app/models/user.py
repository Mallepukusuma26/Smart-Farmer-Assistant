from datetime import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

class UserRole(str, enum.Enum):
    FARMER = 'FARMER'
    ADMIN = 'ADMIN'
    ADVISOR = 'ADVISOR'

class Role(db.Model):
    """User authorization role entity."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    users = db.relationship('User', backref='user_role_obj', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class User(UserMixin, db.Model):
    """Primary User authentication and identity model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='FARMER', index=True)  # FARMER, ADMIN, ADVISOR
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='SET NULL'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)
    timezone = db.Column(db.String(50), default='UTC')
    language_preference = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    farmer_profile = db.relationship('Farmer', backref='user', uselist=False, cascade='all, delete-orphan')
    advisor_profile = db.relationship('Advisor', backref='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')
    user_sessions = db.relationship('UserSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    security_events = db.relationship('SecurityEvent', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set user password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify user password string."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_farmer(self):
        return self.role == 'FARMER'

    def is_advisor(self):
        return self.role == 'ADVISOR'

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.is_locked = False
        self.last_login = datetime.utcnow()

    def record_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.is_locked = True

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'is_locked': self.is_locked,
            'failed_login_attempts': self.failed_login_attempts,
            'timezone': self.timezone,
            'language_preference': self.language_preference,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None
        }

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' role='{self.role}'>"


class UserSession(db.Model):
    """User active login session tracker."""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    device_type = db.Column(db.String(50), default='Desktop')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'device_type': self.device_type,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class SecurityEvent(db.Model):
    """Log of security audit events associated with user identity."""
    __tablename__ = 'security_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    event_type = db.Column(db.String(64), nullable=False, index=True)
    severity = db.Column(db.String(20), default='INFO')  # INFO, WARNING, CRITICAL
    ip_address = db.Column(db.String(45), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'severity': self.severity,
            'ip_address': self.ip_address,
            'details': self.details,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class PasswordResetToken(db.Model):
    """Secure password reset token model."""
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('reset_tokens', lazy='dynamic', cascade='all, delete-orphan'))

    def is_valid(self) -> bool:
        """Check if token is not expired and not used."""
        return not self.is_used and datetime.utcnow() < self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'is_used': self.is_used,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S')
        }

