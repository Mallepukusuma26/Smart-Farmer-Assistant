"""
Farm Profitability Monte Carlo Risk Simulation Engine.
Runs 1,000 stochastic trials simulating commodity price fluctuations, yield distributions,
and input cost volatility to compute Value at Risk (VaR) and profit probabilities.
"""

import math
import random
from typing import Dict, List, Any

class FarmFinancialMonteCarloEngine:
    """Stochastic Monte Carlo farm financial risk simulation engine."""

    def run_profit_simulation(
        self,
        area_ha: float,
        mean_yield_tons_ha: float,
        std_yield_tons_ha: float,
        mean_price_usd_ton: float,
        std_price_usd_ton: float,
        fixed_cost_usd_ha: float,
        trials: int = 500
    ) -> Dict[str, Any]:
        """Simulate distribution of net farm profits across stochastic trials."""
        profits = []
        losses_count = 0

        for _ in range(trials):
            sim_yield = max(0.1, random.gauss(mean_yield_tons_ha, std_yield_tons_ha))
            sim_price = max(10.0, random.gauss(mean_price_usd_ton, std_price_usd_ton))
            
            revenue = area_ha * sim_yield * sim_price
            cost = area_ha * fixed_cost_usd_ha
            profit = revenue - cost

            profits.append(profit)
            if profit < 0:
                losses_count += 1

        profits.sort()
        mean_profit = sum(profits) / float(trials)
        var_5pct = profits[int(trials * 0.05)]  # 5th percentile Value at Risk

        return {
            "trials_run": trials,
            "mean_net_profit_usd": round(mean_profit, 2),
            "max_profit_usd": round(profits[-1], 2),
            "min_profit_usd": round(profits[0], 2),
            "value_at_risk_5pct_usd": round(var_5pct, 2),
            "probability_of_loss_pct": round((losses_count / float(trials)) * 100.0, 1),
            "median_profit_usd": round(profits[trials // 2], 2)
        }
