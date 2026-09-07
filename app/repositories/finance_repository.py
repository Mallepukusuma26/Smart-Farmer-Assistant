from typing import Optional, List, Dict, Any, Tuple
from datetime import date, datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.finance import Expense, Revenue, MarketPrice, CostPerAcre, BudgetPlan
from app.repositories.base_repository import BaseRepository

class FinanceRepository(BaseRepository[Expense]):
    """Data Access Repository for Farm Expenses, Revenue Records, Mandi Market Prices, and Budgeting."""

    def __init__(self):
        super().__init__(Expense)

    def record_expense(self, farmer_id: int, category: str, amount: float, farm_id: Optional[int] = None, field_id: Optional[int] = None, crop_id: Optional[int] = None, quantity: float = 1.0, unit_cost: float = 0.0, payment_method: str = 'Cash', vendor_name: Optional[str] = None, description: Optional[str] = None, expense_date=None) -> Expense:
        """Create itemized farm expense record."""
        if expense_date is None:
            expense_date = date.today()
        exp = Expense(
            farmer_id=farmer_id,
            farm_id=farm_id,
            field_id=field_id,
            crop_id=crop_id,
            category=category,
            amount=amount,
            quantity=quantity,
            unit_cost=unit_cost,
            payment_method=payment_method,
            vendor_name=vendor_name,
            description=description,
            expense_date=expense_date
        )
        db.session.add(exp)
        db.session.commit()
        return exp

    def get_expenses_by_farmer(self, farmer_id: int, start_date=None, end_date=None, category: Optional[str] = None) -> List[Expense]:
        """Fetch all expenses for farmer with optional date and category filters."""
        query = db.session.query(Expense).filter_by(farmer_id=farmer_id)
        if category:
            query = query.filter_by(category=category)
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)
        return query.order_by(Expense.expense_date.desc()).all()

    def calculate_total_expenses(self, farmer_id: int, field_id: Optional[int] = None, start_date=None, end_date=None) -> float:
        """Calculate total expense sum."""
        query = db.session.query(func.sum(Expense.amount)).filter(Expense.farmer_id == farmer_id)
        if field_id:
            query = query.filter(Expense.field_id == field_id)
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)
        total = query.scalar()
        return round(float(total), 2) if total else 0.0

    def record_revenue(self, farmer_id: int, crop_id: int, quantity_sold: float, selling_price_per_unit: float, farm_id: Optional[int] = None, field_id: Optional[int] = None, unit: str = 'Tons', buyer_name: Optional[str] = None, market_mandi_name: Optional[str] = None, payment_status: str = 'Received', sale_date=None, notes: Optional[str] = None) -> Revenue:
        """Create crop harvest sale revenue record."""
        if sale_date is None:
            sale_date = date.today()
        total_rev = round(quantity_sold * selling_price_per_unit, 2)
        rev = Revenue(
            farmer_id=farmer_id,
            farm_id=farm_id,
            field_id=field_id,
            crop_id=crop_id,
            quantity_sold=quantity_sold,
            unit=unit,
            selling_price_per_unit=selling_price_per_unit,
            total_revenue=total_rev,
            buyer_name=buyer_name,
            market_mandi_name=market_mandi_name,
            payment_status=payment_status,
            sale_date=sale_date,
            notes=notes
        )
        db.session.add(rev)
        db.session.commit()
        return rev

    def get_revenues_by_farmer(self, farmer_id: int, start_date=None, end_date=None) -> List[Revenue]:
        """Fetch all revenues for farmer."""
        query = db.session.query(Revenue).filter_by(farmer_id=farmer_id)
        if start_date:
            query = query.filter(Revenue.sale_date >= start_date)
        if end_date:
            query = query.filter(Revenue.sale_date <= end_date)
        return query.order_by(Revenue.sale_date.desc()).all()

    def calculate_total_revenue(self, farmer_id: int, field_id: Optional[int] = None, start_date=None, end_date=None) -> float:
        """Calculate total revenue sum."""
        query = db.session.query(func.sum(Revenue.total_revenue)).filter(Revenue.farmer_id == farmer_id)
        if field_id:
            query = query.filter(Revenue.field_id == field_id)
        if start_date:
            query = query.filter(Revenue.sale_date >= start_date)
        if end_date:
            query = query.filter(Revenue.sale_date <= end_date)
        total = query.scalar()
        return round(float(total), 2) if total else 0.0

    def calculate_net_profit(self, farmer_id: int, field_id: Optional[int] = None, start_date=None, end_date=None) -> float:
        """Calculate net profit = Total Revenue - Total Expenses."""
        rev = self.calculate_total_revenue(farmer_id, field_id, start_date, end_date)
        exp = self.calculate_total_expenses(farmer_id, field_id, start_date, end_date)
        return round(rev - exp, 2)

    def get_market_prices(self, crop_name: Optional[str] = None) -> List[MarketPrice]:
        """Fetch Mandi market price reference indices."""
        query = db.session.query(MarketPrice)
        if crop_name:
            query = query.filter(func.lower(MarketPrice.crop_name) == crop_name.lower().strip())
        return query.order_by(MarketPrice.price_date.desc()).all()

    def set_budget_plan(self, farmer_id: int, season_name: str, year: int, allocated_budget: float) -> BudgetPlan:
        """Set seasonal budget allocation."""
        budget = db.session.query(BudgetPlan).filter_by(farmer_id=farmer_id, season_name=season_name, year=year).first()
        if not budget:
            budget = BudgetPlan(
                farmer_id=farmer_id,
                season_name=season_name,
                year=year,
                allocated_budget=allocated_budget
            )
            db.session.add(budget)
        else:
            budget.allocated_budget = allocated_budget
        db.session.commit()
        return budget
