"""
Search Controller Module for Smart Farmer Assistant.

Provides reusable unified search infrastructure across Farmers, Farms, Fields, Crops,
Fertilizers, Disease Records, Soil Samples, Expenses, Revenue, Irrigation Logs, and Reports.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.search_service import SearchService
import logging

logger = logging.getLogger(__name__)


class SearchController(BaseController):
    """
    Controller handling multi-entity keyword queries, entity category filtering,
    date range filtering, and pagination across all application modules.
    """

    def __init__(self):
        self.search_service = SearchService()

    def search(self) -> Union[str, Tuple[Response, int]]:
        """
        Executes unified search query across all agricultural database tables.
        """
        query = request.args.get("q", request.args.get("query", "")).strip()
        category = request.args.get("category", "all").strip().lower()
        page, per_page = self.parse_pagination_params()

        user_id = self.get_current_user_id()
        results = self.search_service.execute_search(
            query_str=query,
            category=category,
            user_id=user_id,
            is_admin=self.is_admin(),
            page=page,
            per_page=per_page
        )

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=results, message="Search executed successfully")

        return render_template(
            "farmer/search_results.html",
            query=query,
            category=category,
            results=results
        )
