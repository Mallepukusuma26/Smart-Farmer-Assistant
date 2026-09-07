from typing import Optional, List, Dict, Any, Tuple
from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserService:
    """Domain Service for managing user identity, credentials, account activation, and role assignments."""

    def __init__(self, repository: Optional[UserRepository] = None):
        self.repository = repository or UserRepository()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by ID."""
        return self.repository.get_by_id(user_id)

    def update_user_profile(self, user_id: int, timezone: Optional[str] = None, language_preference: Optional[str] = None) -> Optional[User]:
        """Update user preferences."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        kwargs = {}
        if timezone:
            kwargs['timezone'] = timezone
        if language_preference:
            kwargs['language_preference'] = language_preference
        return self.repository.update(user, **kwargs)

    def change_password(self, user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Validate current password and set new password."""
        user = self.repository.get_by_id(user_id)
        if not user or not user.check_password(current_password):
            return False, "Current password verification failed."

        user.set_password(new_password)
        self.repository.save(user)
        return True, "Password updated successfully."

    def toggle_account_active(self, user_id: int) -> Tuple[bool, str]:
        """Activate or deactivate user account (Admin action)."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return False, "User not found."

        user.is_active = not user.is_active
        self.repository.save(user)
        status_str = "activated" if user.is_active else "deactivated"
        return True, f"User account has been {status_str}."

    def search_users(self, keyword: str = "", role_filter: Optional[str] = None, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Paginated user directory search."""
        items, total, pages = self.repository.search_users(keyword=keyword, role_filter=role_filter, page=page, per_page=per_page)
        return {
            'users': [u.to_dict() for u in items],
            'total_items': total,
            'total_pages': pages,
            'current_page': page
        }
