"""
Base Controller Module for Smart Farmer Assistant.

Provides standardized request handling, response formatting, authentication/session
extraction helpers, pagination parsing, and security validation helpers across all web and REST controllers.
"""

from typing import Dict, Any, Tuple, Optional, List, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, current_app, Response
from app.models.user import User, UserRole
import logging
import math

logger = logging.getLogger(__name__)


class BaseController:
    """
    Base controller class providing unified REST API and Web UI response builders,
    error logging, session helpers, parameter sanitization, and pagination metadata logic.
    """

    @staticmethod
    def success_response(
        data: Optional[Any] = None,
        message: str = "Operation completed successfully",
        status_code: int = 200,
        meta: Optional[Dict[str, Any]] = None
    ) -> Tuple[Response, int]:
        """
        Formats a standardized success JSON response payload.
        """
        payload = {
            "success": True,
            "message": message,
            "data": data if data is not None else {}
        }
        if meta:
            payload["meta"] = meta
        return jsonify(payload), status_code

    @staticmethod
    def error_response(
        message: str = "An unexpected error occurred",
        status_code: int = 400,
        errors: Optional[Union[List[str], Dict[str, Any]]] = None,
        error_code: Optional[str] = None
    ) -> Tuple[Response, int]:
        """
        Formats a standardized error JSON response payload.
        """
        payload = {
            "success": False,
            "message": message,
            "errors": errors if errors is not None else [],
            "error_code": error_code or f"ERR_{status_code}"
        }
        return jsonify(payload), status_code

    @staticmethod
    def paginated_response(
        items: List[Any],
        total: int,
        page: int,
        per_page: int,
        message: str = "Records retrieved successfully"
    ) -> Tuple[Response, int]:
        """
        Formats a paginated JSON response payload with complete metadata.
        """
        total_pages = math.ceil(total / per_page) if per_page > 0 else 1
        meta = {
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        return BaseController.success_response(data=items, message=message, status_code=200, meta=meta)

    @staticmethod
    def get_current_user_id() -> Optional[int]:
        """
        Extracts the currently authenticated user ID from Flask session or request context.
        """
        user_id = session.get("user_id")
        if user_id:
            try:
                return int(user_id)
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def get_current_user_role() -> Optional[str]:
        """
        Extracts the currently authenticated user's role from Flask session.
        """
        return session.get("role")

    @staticmethod
    def is_authenticated() -> bool:
        """
        Checks if the current request session is authenticated.
        """
        return "user_id" in session and session.get("user_id") is not None

    @staticmethod
    def is_admin() -> bool:
        """
        Checks if the logged-in user possesses the Admin role.
        """
        return session.get("role") == UserRole.ADMIN.value or session.get("role") == "admin"

    @staticmethod
    def is_farmer() -> bool:
        """
        Checks if the logged-in user possesses the Farmer role.
        """
        return session.get("role") == UserRole.FARMER.value or session.get("role") == "farmer"

    @staticmethod
    def is_advisor() -> bool:
        """
        Checks if the logged-in user possesses the Advisor role.
        """
        return session.get("role") == UserRole.ADVISOR.value or session.get("role") == "advisor"

    @staticmethod
    def parse_pagination_params(default_per_page: int = 15) -> Tuple[int, int]:
        """
        Extracts and validates page and per_page query parameters from the request.
        """
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1

        try:
            per_page = int(request.args.get("per_page", default_per_page))
            if per_page < 1:
                per_page = default_per_page
            elif per_page > 100:
                per_page = 100
        except (ValueError, TypeError):
            per_page = default_per_page

        return page, per_page

    @staticmethod
    def parse_filter_params() -> Dict[str, Any]:
        """
        Parses common search, filter, and sorting query parameters from request string.
        """
        filters = {}
        query = request.args.get("query", request.args.get("q", "")).strip()
        if query:
            filters["query"] = query

        sort_by = request.args.get("sort_by", "").strip()
        if sort_by:
            filters["sort_by"] = sort_by

        order = request.args.get("order", "desc").strip().lower()
        filters["order"] = "asc" if order == "asc" else "desc"

        category = request.args.get("category", "").strip()
        if category:
            filters["category"] = category

        status = request.args.get("status", "").strip()
        if status:
            filters["status"] = status

        date_from = request.args.get("date_from", "").strip()
        if date_from:
            filters["date_from"] = date_from

        date_to = request.args.get("date_to", "").strip()
        if date_to:
            filters["date_to"] = date_to

        return filters

    @staticmethod
    def render_or_json(
        template_name: str,
        context: Dict[str, Any],
        status_code: int = 200
    ) -> Union[str, Tuple[Response, int]]:
        """
        Renders an HTML template if requested via browser navigation or returns JSON
        if the request specifies Accept: application/json or AJAX header.
        """
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.path.startswith("/api/"):
            return BaseController.success_response(data=context, status_code=status_code)
        return render_template(template_name, **context), status_code

    @staticmethod
    def handle_exception(e: Exception, context_msg: str = "An error occurred") -> Tuple[Response, int]:
        """
        Centralized exception handling logging and standard error response generation.
        """
        logger.error(f"{context_msg}: {str(e)}", exc_info=True)
        return BaseController.error_response(
            message=f"{context_msg}: {str(e)}",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR"
        )
