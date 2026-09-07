from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.finance import Expense, Revenue

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
