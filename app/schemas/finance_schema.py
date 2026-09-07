from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.finance import Expense, Revenue

class ExpenseSchema(BaseSchema):
    """Expense model serialization DTO."""
    @staticmethod
    def dump_single(expense: Expense) -> Dict[str, Any]:
        if not expense:
            return {}
        return expense.to_dict()

    @staticmethod
    def dump_many(expenses: List[Expense]) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in expenses] if expenses else []


class RevenueSchema(BaseSchema):
    """Revenue model serialization DTO."""
    @staticmethod
    def dump_single(revenue: Revenue) -> Dict[str, Any]:
        if not revenue:
            return {}
        return revenue.to_dict()

    @staticmethod
    def dump_many(revenues: List[Revenue]) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in revenues] if revenues else []


class FinanceSummarySchema(BaseSchema):
    """Financial summary DTO."""
    @staticmethod
    def dump_summary(total_expenses: float, total_revenue: float, net_profit: float) -> Dict[str, Any]:
        return {
            'total_expenses': round(total_expenses, 2),
            'total_revenue': round(total_revenue, 2),
            'net_profit': round(net_profit, 2),
            'is_profitable': net_profit > 0
        }


class FinanceSchema(BaseSchema):
    """Farm financial expense & revenue serialization DTO."""

    @staticmethod
    def dump_financial_summary(expenses_total: float, revenues_total: float, net_profit: float, itemized_expenses: List[Dict[str, Any]], itemized_revenues: List[Dict[str, Any]]) -> Dict[str, Any]:
        roi_pct = round((net_profit / expenses_total) * 100.0, 2) if expenses_total > 0 else 0.0
        return {
            'summary': {
                'total_expenses': round(expenses_total, 2),
                'total_revenue': round(revenues_total, 2),
                'net_profit': round(net_profit, 2),
                'roi_percent': roi_pct,
                'is_profitable': net_profit > 0
            },
            'expenses': itemized_expenses,
            'revenues': itemized_revenues
        }
