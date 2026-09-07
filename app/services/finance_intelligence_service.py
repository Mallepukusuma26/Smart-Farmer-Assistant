"""
Finance Intelligence Service Module for Smart Farmer Assistant.

Provides comprehensive itemized expense analysis, harvest revenue tracking,
crop-wise profitability indexing, cost-per-acre metrics, ROI calculations, and break-even sales analysis.
"""

from typing import Dict, Any, List, Optional
from app.extensions import db
from app.models.finance import Expense, Revenue
from app.repositories.finance_repository import FinanceRepository


class FinanceIntelligenceService:
    """
    Advanced financial analytics engine for cost breakdown, revenue accounting,
    ROI percentage modeling, and break-even harvest market pricing.
    """

    def __init__(self, repository: Optional[FinanceRepository] = None):
        self.repository = repository or FinanceRepository()

    def get_farmer_financial_metrics(self, farmer_id: int, total_acres: float = 1.0) -> Dict[str, Any]:
        """
        Calculates itemized cost breakdown, total revenue, net margin, and cost per acre.
        """
        expenses = db.session.query(Expense).filter_by(farmer_id=farmer_id).all()
        revenues = db.session.query(Revenue).filter_by(farmer_id=farmer_id).all()

        total_exp = sum(float(e.amount or 0.0) for e in expenses)
        total_rev = sum(float(r.total_amount or (r.quantity_sold * r.selling_price_per_unit) or 0.0) for r in revenues)
        net_profit = total_rev - total_exp

        area = max(0.1, total_acres)
        cost_per_acre = round(total_exp / area, 2)
        rev_per_acre = round(total_rev / area, 2)
        profit_per_acre = round(net_profit / area, 2)

        roi_pct = round((net_profit / total_exp) * 100.0, 2) if total_exp > 0 else 0.0
        margin_pct = round((net_profit / total_rev) * 100.0, 2) if total_rev > 0 else 0.0

        category_breakdown = {}
        for e in expenses:
            cat = e.category or "General"
            category_breakdown[cat] = category_breakdown.get(cat, 0.0) + float(e.amount or 0.0)

        formatted_categories = [
            {"category": k, "amount": round(v, 2), "pct": round((v / total_exp) * 100.0, 1) if total_exp > 0 else 0.0}
            for k, v in category_breakdown.items()
        ]

        return {
            "farmer_id": farmer_id,
            "total_land_acres": area,
            "total_expenses": round(total_exp, 2),
            "total_revenue": round(total_rev, 2),
            "net_profit": round(net_profit, 2),
            "cost_per_acre": cost_per_acre,
            "revenue_per_acre": rev_per_acre,
            "profit_per_acre": profit_per_acre,
            "roi_percentage": roi_pct,
            "profit_margin_percentage": margin_pct,
            "is_profitable": net_profit >= 0,
            "itemized_category_breakdown": formatted_categories
        }

    def calculate_breakeven_price(self, total_cost: float, expected_yield_quintals: float) -> Dict[str, Any]:
        """
        Calculates minimum market price per quintal required to break even.
        """
        if expected_yield_quintals <= 0:
            return {"error": "Yield quintals must be greater than zero."}

        breakeven_price = round(total_cost / expected_yield_quintals, 2)
        target_margin_15 = round(breakeven_price * 1.15, 2)
        target_margin_30 = round(breakeven_price * 1.30, 2)

        return {
            "total_cost_inr": round(total_cost, 2),
            "expected_yield_quintals": expected_yield_quintals,
            "breakeven_price_per_quintal_inr": breakeven_price,
            "suggested_mandi_price_15pct_profit": target_margin_15,
            "suggested_mandi_price_30pct_profit": target_margin_30
        }
