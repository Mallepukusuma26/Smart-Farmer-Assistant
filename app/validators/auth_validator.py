from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class LoginValidator(BaseValidator):
    """Validator for user authentication login requests."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['username_or_email', 'password'])
        username_or_email = self.sanitize_string('username_or_email', max_length=120)
        password = self.data.get('password', '')

        if len(password) < 6:
            self.add_error('password', 'Password must be at least 6 characters long.')

        if not self.is_valid():
            return {}

        return {
            'username_or_email': username_or_email,
            'password': password
        }


class RegistrationValidator(BaseValidator):
    """Validator for user registration requests."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['username', 'email', 'password', 'confirm_password', 'role'])
        username = self.sanitize_string('username', max_length=64)
        email = self.validate_email('email')
        password = self.data.get('password', '')
        confirm_password = self.data.get('confirm_password', '')
        role = self.validate_choice('role', ['FARMER', 'ADVISOR', 'ADMIN'])

        if username and len(username) < 3:
            self.add_error('username', 'Username must be at least 3 characters long.')

        if password and len(password) < 8:
            self.add_error('password', 'Password must be at least 8 characters long.')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        if not self.is_valid():
            return {}

        return {
            'username': username,
            'email': email,
            'password': password,
            'role': role
        }


class PasswordResetValidator(BaseValidator):
    """Validator for password reset workflows."""

    def validate_request(self) -> Optional[str]:
        self.validate_required(['email'])
        return self.validate_email('email')

    def validate_confirm(self) -> Optional[str]:
        self.validate_required(['token', 'new_password', 'confirm_password'])
        new_pass = self.data.get('new_password', '')
        conf_pass = self.data.get('confirm_password', '')

        if len(new_pass) < 8:
            self.add_error('new_password', 'Password must be at least 8 characters.')

        if new_pass != conf_pass:
            self.add_error('confirm_password', 'Passwords do not match.')

        return new_pass if self.is_valid() else None


class AuthValidator:
    """Unified authentication request validator."""

    @staticmethod
    def validate_login(data: Dict[str, Any]) -> Dict[str, Any]:
        val = LoginValidator(data)
        return val.validate()

    @staticmethod
    def validate_registration(data: Dict[str, Any]) -> Dict[str, Any]:
        val = RegistrationValidator(data)
        return val.validate()

