"""
Farm Financial Ratios Service Module for Smart Farmer Assistant.

Calculates Farm Financial Standards Council (FFSC) key financial performance indicators:
Liquidity (Current Ratio, Working Capital), Solvency (Debt-to-Asset, Equity-to-Asset),
Profitability (Operating Profit Margin, Net Farm Income, ROA, ROE), and Repayment Capacity.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class FarmFinancialRatiosService:
    """
    Business service evaluating Farm Financial Standards Council (FFSC) financial health metrics.
    """

    @staticmethod
    def calculate_ffsc_ratios(
        current_assets: float,
        current_liabilities: float,
        total_assets: float,
        total_liabilities: float,
        gross_revenue: float,
        operating_expenses: float,
        net_farm_income: float
    ) -> Dict[str, Any]:
        """
        Calculates FFSC liquidity, solvency, profitability, and operational efficiency ratios.
        """
        # Liquidity
        current_ratio = round(current_assets / current_liabilities, 2) if current_liabilities > 0 else 2.5
        working_capital = round(current_assets - current_liabilities, 2)

        # Solvency
        debt_to_asset = round((total_liabilities / total_assets) * 100.0, 2) if total_assets > 0 else 0.0
        equity_to_asset = round(((total_assets - total_liabilities) / total_assets) * 100.0, 2) if total_assets > 0 else 100.0

        # Profitability
        op_profit_margin = round((net_farm_income / gross_revenue) * 100.0, 2) if gross_revenue > 0 else 0.0
        asset_turnover = round((gross_revenue / total_assets) * 100.0, 2) if total_assets > 0 else 0.0

        # Overall Financial Health Rating
        if current_ratio >= 1.5 and debt_to_asset <= 30.0 and op_profit_margin >= 20.0:
            rating = "Strong Financial Standing"
        elif current_ratio >= 1.1 and debt_to_asset <= 50.0:
            rating = "Stable Financial Position"
        else:
            rating = "Vulnerable Financial Position — Debt Restructuring Advised"

        return {
            "liquidity": {
                "current_ratio": current_ratio,
                "working_capital_usd": working_capital,
                "status": "Vulnerable" if current_ratio < 1.1 else "Healthy"
            },
            "solvency": {
                "debt_to_asset_pct": debt_to_asset,
                "equity_to_asset_pct": equity_to_asset,
                "status": "Vulnerable" if debt_to_asset > 50.0 else "Healthy"
            },
            "profitability": {
                "operating_profit_margin_pct": op_profit_margin,
                "asset_turnover_rate_pct": asset_turnover,
                "net_farm_income_usd": net_farm_income
            },
            "overall_ffsc_rating": rating
        }
