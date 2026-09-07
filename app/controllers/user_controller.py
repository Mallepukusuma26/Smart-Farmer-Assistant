"""
User Controller Module for Smart Farmer Assistant.

Manages generic user profile retrieval, settings, password changes, contact information,
and role verification across all role types.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
import logging

logger = logging.getLogger(__name__)


class UserController(BaseController):
    """
    Controller handling general user account operations, profile editing, and account details.
    """

    def __init__(self):
        self.user_service = UserService()
        self.user_schema = UserSchema()

    def get_current_user_profile(self) -> Union[str, Tuple[Response, int]]:
        """
        Returns currently authenticated user profile.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return self.error_response(message="User account not found", status_code=404)

        serialized = self.user_schema.dump_single(user)
        return self.render_or_json("auth/profile.html", {"user": user, "user_data": serialized})
