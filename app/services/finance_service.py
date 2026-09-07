from datetime import datetime
from sqlalchemy import func
from app.extensions import db
from app.models.finance import Expense, Revenue

class FinanceService:
    """Service layer for farm expense tracking, harvest revenue, and financial analytics."""

    @staticmethod
    def add_expense(farmer_id, category, amount, description=None, farm_id=None, field_id=None, expense_date=None):
        """Add farm expense item."""
        exp = Expense(
            farmer_id=farmer_id,
            farm_id=farm_id,
            field_id=field_id,
            category=category,
            amount=float(amount),
            description=description,
            expense_date=expense_date or datetime.utcnow().date()
        )
        db.session.add(exp)
        db.session.commit()
        return exp

    @staticmethod
    def add_revenue(farmer_id, crop_id, quantity_sold, selling_price_per_unit, buyer_name=None, farm_id=None, field_id=None, unit='Tons', sale_date=None, notes=None):
        """Add harvest revenue sale item."""
        qty = float(quantity_sold)
        price = float(selling_price_per_unit)
        total = qty * price

        rev = Revenue(
            farmer_id=farmer_id,
            farm_id=farm_id,
            field_id=field_id,
            crop_id=crop_id,
            quantity_sold=qty,
            unit=unit,
            selling_price_per_unit=price,
            total_revenue=total,
            buyer_name=buyer_name,
            sale_date=sale_date or datetime.utcnow().date(),
            notes=notes
        )
        db.session.add(rev)
        db.session.commit()
        return rev

    @staticmethod
    def get_financial_summary(farmer_id):
        """Get total expenses, total revenue, net profit, and expense category breakdown."""
        total_exp = db.session.query(func.sum(Expense.amount)).filter_by(farmer_id=farmer_id).scalar() or 0.0
        total_rev = db.session.query(func.sum(Revenue.total_revenue)).filter_by(farmer_id=farmer_id).scalar() or 0.0
        net_profit = total_rev - total_exp
        profit_margin = (net_profit / max(total_rev, 1.0)) * 100.0 if total_rev > 0 else 0.0

        # Category breakdown
        category_rows = db.session.query(
            Expense.category, func.sum(Expense.amount)
        ).filter_by(farmer_id=farmer_id).group_by(Expense.category).all()

        categories = {cat: float(amt) for cat, amt in category_rows}

        return {
            'total_expense': round(float(total_exp), 2),
            'total_revenue': round(float(total_rev), 2),
            'net_profit': round(float(net_profit), 2),
            'profit_margin_percent': round(float(profit_margin), 2),
            'category_breakdown': categories
        }
