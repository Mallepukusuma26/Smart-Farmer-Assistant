from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.user import User, UserSession, SecurityEvent

class UserSchema(BaseSchema):
    """User serialization schema DTO."""

    @staticmethod
    def dump_user(user: Optional[User], include_profile: bool = True) -> Dict[str, Any]:
        if not user:
            return {}
        data = user.to_dict()
        if include_profile:
            if user.farmer_profile:
                data['farmer_profile'] = user.farmer_profile.to_dict()
            if user.advisor_profile:
                data['advisor_profile'] = user.advisor_profile.to_dict()
        return data

    @staticmethod
    def dump_auth_token_response(user: User, token: str, expires_at) -> Dict[str, Any]:
        return {
            'user': UserSchema.dump_user(user),
            'access_token': token,
            'token_type': 'Bearer',
            'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(expires_at, 'strftime') else str(expires_at)
        }
