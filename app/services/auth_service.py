from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.models.farmer import Farmer
from app.models.advisor import Advisor

class AuthService:
    """Service layer for authentication, registration, and user session management."""

    @staticmethod
    def register_user(username, email, password, role='FARMER', full_name=None, phone=None, address=None, region=None):
        """Register a new user account with role profile."""
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return None, "Username or Email already registered."

        user = User(username=username, email=email, role=role.upper())
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        if user.role == 'FARMER':
            farmer = Farmer(
                user_id=user.id,
                full_name=full_name or username,
                phone=phone,
                address=address,
                region=region or 'Default Region'
            )
            db.session.add(farmer)
        elif user.role == 'ADVISOR':
            advisor = Advisor(
                user_id=user.id,
                full_name=full_name or username,
                phone=phone,
                region=region or 'Default Region'
            )
            db.session.add(advisor)

        db.session.commit()
        return user, "Registration successful."

    @staticmethod
    def authenticate_user(username_or_email, password):
        """Authenticate user credentials with login attempt tracking."""
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if not user:
            return None, "Invalid credentials."

        if user.is_locked:
            return None, "Account is locked due to multiple failed login attempts. Contact Admin."

        if not user.is_active:
            return None, "Account is deactivated. Please contact support."

        if user.check_password(password):
            user.failed_login_attempts = 0
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user, "Login successful."
        else:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
            db.session.commit()
            return None, "Invalid credentials."

    @staticmethod
    def change_password(user_id, current_password, new_password):
        """Change user password."""
        user = User.query.get(user_id)
        if not user or not user.check_password(current_password):
            return False, "Current password incorrect."

        user.set_password(new_password)
        db.session.commit()
        return True, "Password updated successfully."

    @staticmethod
    def update_profile(user_id, full_name, phone=None, address=None, region=None):
        """Update user profile information."""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        if user.farmer_profile:
            user.farmer_profile.full_name = full_name
            user.farmer_profile.phone = phone
            user.farmer_profile.address = address
            user.farmer_profile.region = region
        elif user.advisor_profile:
            user.advisor_profile.full_name = full_name
            user.advisor_profile.phone = phone
            user.advisor_profile.region = region

        db.session.commit()
        return True, "Profile updated successfully."
