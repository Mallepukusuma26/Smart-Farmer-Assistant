"""
Finance Controller Module for Smart Farmer Assistant.

Manages farm financial ledger, operational expense tracking (seeds, fertilizers, pesticides,
labour, irrigation, machinery, transport), crop/field harvest revenue logging, net profit/loss,
ROI percentages, cost-per-acre analysis, and monthly/yearly financial summaries.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.finance_service import FinanceService
from app.services.farmer_service import FarmerService
from app.services.farm_service import FarmService
from app.services.field_service import FieldService
from app.services.audit_service import AuditService
from app.validators.finance_validator import ExpenseValidator, RevenueValidator
from app.schemas.finance_schema import ExpenseSchema, RevenueSchema, FinanceSummarySchema
import logging

logger = logging.getLogger(__name__)


class FinanceController(BaseController):
    """
    Controller handling farm income statement ledger, categorized expenses,
    harvest revenue tracking, net profit margin computation, and financial reporting.
    """

    def __init__(self):
        self.finance_service = FinanceService()
        self.farmer_service = FarmerService()
        self.farm_service = FarmService()
        self.field_service = FieldService()
        self.audit_service = AuditService()
        self.expense_validator = ExpenseValidator()
        self.revenue_validator = RevenueValidator()
        self.expense_schema = ExpenseSchema()
        self.revenue_schema = RevenueSchema()
        self.summary_schema = FinanceSummarySchema()

    def get_financial_summary(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders complete financial summary statement including total income, itemized expenses,
        net profit/loss, return on investment (ROI %), cost-per-acre, and profit-per-acre.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            summary = self.finance_service.get_empty_summary()
        else:
            year = request.args.get("year", type=int)
            farm_id = request.args.get("farm_id", type=int)
            summary = self.finance_service.get_financial_summary_by_farmer(farmer.id, year=year, farm_id=farm_id)

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=summary)

        farms = self.farm_service.get_farms_by_farmer_id(farmer.id) if farmer else []
        return render_template(
            "farmer/expenses.html",
            summary=summary,
            farms=farms
        )

    def list_expenses(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists itemized farm expenses with filtering by category, date range, or farm.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            expenses, total = [], 0
        else:
            expenses, total = self.finance_service.get_expenses_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.expense_schema.dump_list(expenses)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/expenses.html",
            expenses=expenses,
            expenses_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def add_expense(self) -> Union[str, Tuple[Response, int]]:
        """
        Records a new farm operation expense transaction.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            farmer = self.farmer_service.create_farmer_profile_for_user(user_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        data["farmer_id"] = farmer.id

        is_valid, validation_errors = self.expense_validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.list_expenses"))

        try:
            expense = self.finance_service.add_expense(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="EXPENSE_ADDED",
                entity_type="Expense",
                entity_id=expense.id,
                details={"category": expense.category, "amount": float(expense.amount)}
            )

            serialized = self.expense_schema.dump_single(expense)
            if request.is_json:
                return self.success_response(data=serialized, message="Expense recorded successfully", status_code=201)

            flash(f"Recorded expense of ${expense.amount} for {expense.category}", "success")
            return redirect(url_for("farmer.list_expenses"))

        except Exception as e:
            return self.handle_exception(e, "Error adding expense transaction")

    def list_revenue(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists crop harvest sales revenue entries.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            revenues, total = [], 0
        else:
            revenues, total = self.finance_service.get_revenue_by_farmer_paginated(farmer.id, page=page, per_page=per_page, filters=filters)

        serialized = self.revenue_schema.dump_list(revenues)
        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "farmer/revenue.html",
            revenues=revenues,
            revenues_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def add_revenue(self) -> Union[str, Tuple[Response, int]]:
        """
        Records a new crop harvest sales revenue entry.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        farmer = self.farmer_service.get_farmer_by_user_id(user_id)
        if not farmer:
            farmer = self.farmer_service.create_farmer_profile_for_user(user_id)

        data = request.get_json() if request.is_json else request.form.to_dict()
        data["farmer_id"] = farmer.id

        is_valid, validation_errors = self.revenue_validator.validate(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("farmer.list_revenue"))

        try:
            revenue = self.finance_service.add_revenue(data)
            self.audit_service.log_event(
                user_id=user_id,
                action="REVENUE_ADDED",
                entity_type="Revenue",
                entity_id=revenue.id,
                details={"crop_name": revenue.crop_name, "total_revenue": float(revenue.total_revenue)}
            )

            serialized = self.revenue_schema.dump_single(revenue)
            if request.is_json:
                return self.success_response(data=serialized, message="Revenue recorded successfully", status_code=201)

            flash(f"Recorded revenue of ${revenue.total_revenue} for {revenue.crop_name}", "success")
            return redirect(url_for("farmer.list_revenue"))

        except Exception as e:
            return self.handle_exception(e, "Error adding revenue transaction")
