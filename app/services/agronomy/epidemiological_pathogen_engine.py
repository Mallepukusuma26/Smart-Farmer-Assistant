"""
Plant Disease SIR Epidemiological Pathogen Engine.
Simulates Susceptible-Infectious-Removed (SIR) plant disease spread,
spore germination probability, and leaf wetness duration (LWD) risk indices.
"""

import math
from typing import Dict, Any, List

class EpidemiologicalPathogenEngine:
    """Plant pathogen epidemiological model and leaf wetness spore germination calculator."""

    def __init__(self):
        pass

    def calculate_spore_germination_probability(
        self, temp_c: float, leaf_wetness_hours: float, pathogen_type: str = "fungal"
    ) -> float:
        """
        Calculate germination probability for plant fungal pathogens (e.g., Phytophthora, Puccinia, Blumeria).
        Uses Yan and Hunt cardinal temperature equation combined with leaf wetness duration.
        """
        # Cardinal temperatures for typical fungal pathogen (T_min=5, T_opt=22, T_max=35)
        t_min, t_opt, t_max = 5.0, 22.0, 35.0
        
        if temp_c <= t_min or temp_c >= t_max:
            temp_suitability = 0.0
        else:
            temp_suitability = ((t_max - temp_c) / (t_max - t_opt)) * ((temp_c - t_min) / (t_opt - t_min)) ** ((t_opt - t_min) / (t_max - t_opt))

        # Wetness duration requirement (minimum 4h, optimal >12h)
        if leaf_wetness_hours < 2.0:
            wetness_factor = 0.0
        elif leaf_wetness_hours < 12.0:
            wetness_factor = (leaf_wetness_hours - 2.0) / 10.0
        else:
            wetness_factor = 1.0

        germination_prob = temp_suitability * wetness_factor
        return round(max(0.0, min(1.0, germination_prob)), 3)

    def simulate_sir_disease_progression(
        self,
        total_plants: int,
        initial_infected: int,
        transmission_rate_beta: float,
        recovery_rate_gamma: float,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Simulate SIR plant disease spread across a field trajectory.
        S: Susceptible plant count, I: Infected plant count, R: Removed/Treated plant count.
        """
        S = float(total_plants - initial_infected)
        I = float(initial_infected)
        R = 0.0
        N = float(total_plants)

        trajectory = []
        
        for day in range(1, days + 1):
            new_infections = (transmission_rate_beta * S * I) / N
            new_recoveries = recovery_rate_gamma * I

            new_infections = min(S, new_infections)
            new_recoveries = min(I, new_recoveries)

            S -= new_infections
            I += (new_infections - new_recoveries)
            R += new_recoveries

            trajectory.append({
                "day": day,
                "susceptible": int(round(S)),
                "infected": int(round(I)),
                "removed": int(round(R)),
                "infection_rate_pct": round((I / N) * 100.0, 2)
            })

        r0 = transmission_rate_beta / max(0.001, recovery_rate_gamma)

        return {
            "total_plants": total_plants,
            "basic_reproduction_number_r0": round(r0, 2),
            "epidemic_risk_level": "High" if r0 > 1.5 else ("Moderate" if r0 >= 1.0 else "Low"),
            "peak_infected_count": max(step["infected"] for step in trajectory),
            "trajectory": trajectory
        }
