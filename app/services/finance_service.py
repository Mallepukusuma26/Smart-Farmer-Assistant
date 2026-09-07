from typing import Dict, Any, List, Optional
from datetime import date, datetime
from app.repositories.finance_repository import FinanceRepository
from app.models.finance import Expense, Revenue, MarketPrice

class FinanceService:
    """Domain Service for farm financial accounting, expense categorizations, revenue sales tracking, and P&L analytics."""

    def __init__(self, repository: Optional[FinanceRepository] = None):
        self.repository = repository or FinanceRepository()

    @staticmethod
    def add_expense(
        farmer_id: int,
        category: str,
        amount: float,
        description: Optional[str] = None,
        farm_id: Optional[int] = None,
        field_id: Optional[int] = None,
        crop_id: Optional[int] = None,
        quantity: float = 1.0,
        unit_cost: float = 0.0,
        payment_method: str = 'Cash',
        vendor_name: Optional[str] = None,
        expense_date=None
    ) -> Expense:
        """Add itemized farm expense transaction."""
        repo = FinanceRepository()
        return repo.record_expense(
            farmer_id=farmer_id,
            category=category,
            amount=amount,
            farm_id=farm_id,
            field_id=field_id,
            crop_id=crop_id,
            quantity=quantity,
            unit_cost=unit_cost,
            payment_method=payment_method,
            vendor_name=vendor_name,
            description=description,
            expense_date=expense_date
        )

    @staticmethod
    def add_revenue(
        farmer_id: int,
        crop_id: int,
        quantity_sold: float,
        selling_price_per_unit: float,
        buyer_name: Optional[str] = None,
        farm_id: Optional[int] = None,
        field_id: Optional[int] = None,
        unit: str = 'Ton',
        market_mandi_name: Optional[str] = None,
        payment_status: str = 'Received',
        sale_date=None,
        notes: Optional[str] = None
    ) -> Revenue:
        """Add harvest revenue sale record."""
        repo = FinanceRepository()
        return repo.record_revenue(
            farmer_id=farmer_id,
            crop_id=crop_id,
            quantity_sold=quantity_sold,
            selling_price_per_unit=selling_price_per_unit,
            farm_id=farm_id,
            field_id=field_id,
            unit=unit,
            buyer_name=buyer_name,
            market_mandi_name=market_mandi_name,
            payment_status=payment_status,
            sale_date=sale_date,
            notes=notes
        )

    @staticmethod
    def get_financial_summary(farmer_id: int, total_land_acres: float = 1.0) -> Dict[str, Any]:
        """Compute full farm financial summary including P&L, ROI %, Cost/Acre, and category breakdowns."""
        repo = FinanceRepository()
        total_exp = repo.calculate_total_expenses(farmer_id)
        total_rev = repo.calculate_total_revenue(farmer_id)
        net_profit = total_rev - total_exp
        profit_margin = round((net_profit / total_rev) * 100.0, 2) if total_rev > 0 else 0.0
        roi_percent = round((net_profit / total_exp) * 100.0, 2) if total_exp > 0 else 0.0

        acres = max(0.1, total_land_acres)
        cost_per_acre = round(total_exp / acres, 2)
        revenue_per_acre = round(total_rev / acres, 2)
        profit_per_acre = round(net_profit / acres, 2)

        # Expense breakdown by category
        expenses = repo.get_expenses_by_farmer(farmer_id)
        category_totals: Dict[str, float] = {}
        for exp in expenses:
            category_totals[exp.category] = round(category_totals.get(exp.category, 0.0) + exp.amount, 2)

        category_breakdown = [{'category': k, 'amount': v, 'percentage': round((v / total_exp) * 100.0, 1) if total_exp > 0 else 0.0} for k, v in category_totals.items()]
        revenues = repo.get_revenues_by_farmer(farmer_id)

        return {
            'total_expense': round(total_exp, 2),
            'total_expenses': round(total_exp, 2),
            'total_revenue': round(total_rev, 2),
            'net_profit': round(net_profit, 2),
            'overview': {
                'total_expenses': round(total_exp, 2),
                'total_revenue': round(total_rev, 2),
                'net_profit': round(net_profit, 2),
                'profit_margin_pct': profit_margin,
                'roi_pct': roi_percent,
                'is_profitable': net_profit >= 0,
                'cost_per_acre': cost_per_acre,
                'revenue_per_acre': revenue_per_acre,
                'profit_per_acre': profit_per_acre
            },
            'category_breakdown': category_breakdown,
            'recent_expenses': [e.to_dict() for e in expenses[:10]],
            'recent_revenues': [r.to_dict() for r in revenues[:10]]
        }
