from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.user import User, Role, UserSession, SecurityEvent, PasswordResetToken
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """Data Access Repository for User, Role, Session, and Security Management."""

    def __init__(self):
        super().__init__(User)

    def find_by_username(self, username: str) -> Optional[User]:
        """Look up user by exact username."""
        return db.session.query(User).filter(func.lower(User.username) == username.lower().strip()).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Look up user by exact email address."""
        return db.session.query(User).filter(func.lower(User.email) == email.lower().strip()).first()

    def find_by_username_or_email(self, login_identifier: str) -> Optional[User]:
        """Look up user by username OR email."""
        ident = login_identifier.lower().strip()
        return db.session.query(User).filter(
            or_(func.lower(User.username) == ident, func.lower(User.email) == ident)
        ).first()

    def get_users_by_role(self, role_name: str) -> List[User]:
        """Fetch all users assigned to a specific role."""
        return db.session.query(User).filter(User.role == role_name.upper()).all()

    def search_users(self, keyword: str, role_filter: Optional[str] = None, page: int = 1, per_page: int = 20) -> Tuple[List[User], int, int]:
        """Search users by username or email with optional role filtering."""
        query = db.session.query(User)
        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(or_(User.username.ilike(term), User.email.ilike(term)))
        if role_filter:
            query = query.filter(User.role == role_filter.upper())
        return self.paginate(page=page, per_page=per_page, query=query.order_by(User.created_at.desc()))

    def lock_user_account(self, user_id: int) -> bool:
        """Lock user account due to repeated security failures."""
        user = self.get_by_id(user_id)
        if user:
            user.is_locked = True
            db.session.commit()
            return True
        return False

    def unlock_user_account(self, user_id: int) -> bool:
        """Unlock locked user account."""
        user = self.get_by_id(user_id)
        if user:
            user.is_locked = False
            user.failed_login_attempts = 0
            db.session.commit()
            return True
        return False

    def record_login_attempt(self, user_id: int, success: bool, ip_address: Optional[str] = None) -> User:
        """Record login attempt success or failure."""
        user = self.get_by_id(user_id)
        if user:
            if success:
                user.reset_failed_login()
            else:
                user.record_failed_login()
            db.session.commit()
        return user

    def create_user_session(self, user_id: int, session_token: str, ip_address: str, user_agent: str, expires_at) -> UserSession:
        """Create new active user session log."""
        session = UserSession(
            user_id=user_id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )
        db.session.add(session)
        db.session.commit()
        return session

    def get_active_sessions(self, user_id: int) -> List[UserSession]:
        """Fetch all active login sessions for a user."""
        return db.session.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).all()

    def invalidate_session(self, session_token: str) -> bool:
        """Mark session token inactive."""
        session = db.session.query(UserSession).filter_by(session_token=session_token).first()
        if session:
            session.is_active = False
            db.session.commit()
            return True
        return False

    def create_security_event(self, user_id: Optional[int], event_type: str, severity: str, ip_address: str, details: str) -> SecurityEvent:
        """Log security audit event."""
        event = SecurityEvent(
            user_id=user_id,
            event_type=event_type,
            severity=severity,
            ip_address=ip_address,
            details=details
        )
        db.session.add(event)
        db.session.commit()
        return event

    def create_reset_token(self, user_id: int, token: str, expires_at) -> PasswordResetToken:
        """Issue password reset token."""
        reset_token = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(reset_token)
        db.session.commit()
        return reset_token

    def verify_reset_token(self, token: str) -> Optional[PasswordResetToken]:
        """Verify and fetch password reset token if valid."""
        reset_tok = db.session.query(PasswordResetToken).filter_by(token=token).first()
        if reset_tok and reset_tok.is_valid():
            return reset_tok
        return None
