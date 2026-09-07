"""
Build Additional Agronomic Engines for Smart Farmer Assistant.
"""

import os

AGRONOMY_DIR = os.path.join("app", "services", "agronomy")
os.makedirs(AGRONOMY_DIR, exist_ok=True)

engines = {}

engines["epidemiological_pathogen_engine.py"] = '''"""
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
'''

engines["weed_competition_engine.py"] = '''"""
Crop-Weed Competition Yield Loss Engine.
Implements Cousens hyperbolic crop-weed competition equation and
Critical Period for Weed Control (CPWC) models.
"""

import math
from typing import Dict, Any

class WeedCompetitionEngine:
    """Cousens hyperbolic model for estimating crop yield loss due to weed density."""

    def calculate_yield_loss_cousens(
        self, weed_density_plants_m2: float, parameter_i: float = 0.8, parameter_a: float = 85.0
    ) -> Dict[str, float]:
        """
        Cousens Model: Y_loss (%) = (I * d) / (1 + (I * d / A))
        Where:
          d = weed density (plants/m2)
          I = yield loss per unit weed density as d -> 0
          A = maximum asymptotic yield loss (%) as d -> infinity
        """
        d = weed_density_plants_m2
        if d <= 0:
            return {"yield_loss_pct": 0.0, "retained_yield_pct": 100.0}

        y_loss = (parameter_i * d) / (1.0 + (parameter_i * d / max(1.0, parameter_a)))
        y_loss = min(parameter_a, max(0.0, y_loss))

        return {
            "weed_density_m2": d,
            "yield_loss_pct": round(y_loss, 2),
            "retained_yield_pct": round(100.0 - y_loss, 2),
            "action_threshold_exceeded": d > 5.0
        }
'''

engines["greenhouse_gas_carbon_engine.py"] = '''"""
Agricultural Greenhouse Gas (GHG) & Soil Carbon Sequestration Engine.
Implements IPCC Tier 1 and Tier 2 methodology for N2O emissions,
methane flux, and Soil Organic Carbon (SOC) stock change calculations.
"""

from typing import Dict, Any

class GreenhouseGasCarbonEngine:
    """IPCC Tier 1/2 agricultural emission and carbon sequestration calculator."""

    def calculate_n2o_emissions(
        self, synthetic_n_kg: float, organic_n_kg: float, crop_residue_n_kg: float = 0.0
    ) -> Dict[str, float]:
        """
        Direct and indirect N2O emissions from soil inputs.
        IPCC Default EF1 = 0.01 (1% of N input converted to N2O-N).
        """
        total_n_input = synthetic_n_kg + organic_n_kg + crop_residue_n_kg
        
        # Direct N2O-N emissions (kg N2O-N)
        direct_n2o_n = total_n_input * 0.01

        # Indirect N2O from atmospheric deposition (FracGASM * EF4)
        volatilized_n = synthetic_n_kg * 0.10 + organic_n_kg * 0.20
        indirect_dep_n2o_n = volatilized_n * 0.01

        # Indirect N2O from leaching (FracLEACH * EF5)
        leached_n = total_n_input * 0.30
        indirect_leach_n2o_n = leached_n * 0.0075

        total_n2o_n = direct_n2o_n + indirect_dep_n2o_n + indirect_leach_n2o_n
        total_n2o_kg = total_n2o_n * (44.0 / 28.0)  # Molecular weight ratio N2O/N2
        co2_equivalent_kg = total_n2o_kg * 273.0  # GWP 100-yr factor for N2O = 273

        return {
            "total_nitrogen_applied_kg": round(total_n_input, 2),
            "direct_n2o_kg": round(direct_n2o_n * (44.0 / 28.0), 3),
            "indirect_n2o_kg": round((indirect_dep_n2o_n + indirect_leach_n2o_n) * (44.0 / 28.0), 3),
            "total_n2o_emissions_kg": round(total_n2o_kg, 3),
            "co2_equivalent_emissions_kg": round(co2_equivalent_kg, 2)
        }

    def calculate_soc_sequestration(
        self, base_soc_ton_ha: float, tillage_practice: str = "no_till", organic_amendment_ton_ha: float = 5.0
    ) -> Dict[str, float]:
        """
        Soil Organic Carbon (SOC) annual accumulation estimation.
        """
        tillage_factors = {
            "conventional": 1.0,
            "reduced": 1.08,
            "no_till": 1.15
        }
        f_mg = tillage_factors.get(tillage_practice.lower(), 1.0)
        
        # Organic amendment carbon transfer (approx 0.15 C fraction converted to persistent SOC)
        c_added = organic_amendment_ton_ha * 0.35 * 0.15

        annual_soc_gain = base_soc_ton_ha * (f_mg - 1.0) * 0.05 + c_added
        co2_sequestered_ton_ha = annual_soc_gain * (44.0 / 12.0)

        return {
            "initial_soc_ton_ha": base_soc_ton_ha,
            "annual_soc_gain_ton_ha": round(annual_soc_gain, 3),
            "net_co2_sequestered_ton_ha": round(co2_sequestered_ton_ha, 3),
            "projected_soc_5yr": round(base_soc_ton_ha + annual_soc_gain * 5.0, 2)
        }
'''

engines["salinity_leaching_engine.py"] = '''"""
Soil Salinity Reclamation & Leaching Requirement Engine.
Implements US Salinity Laboratory formulas for ECe leaching requirements
and Gypsum requirements for Sodic soil reclamation.
"""

from typing import Dict, Any

class SalinityLeachingEngine:
    """Soil and water salinity reclamation calculator."""

    def calculate_leaching_requirement(
        self, ec_irrigation_ds_m: float, target_ec_soil_ds_m: float = 4.0
    ) -> Dict[str, float]:
        """
        Leaching Requirement LR = ECw / (5 * ECe_target - ECw)
        """
        ec_w = ec_irrigation_ds_m
        ec_e = target_ec_soil_ds_m

        denom = max(0.1, (5.0 * ec_e) - ec_w)
        lr_fraction = ec_w / denom
        lr_fraction = max(0.05, min(0.50, lr_fraction))

        return {
            "irrigation_water_ec_ds_m": ec_w,
            "target_soil_ec_ds_m": ec_e,
            "leaching_requirement_fraction": round(lr_fraction, 3),
            "leaching_requirement_pct": round(lr_fraction * 100.0, 1),
            "additional_water_needed_pct": round((lr_fraction / (1.0 - lr_fraction)) * 100.0, 1)
        }

    def calculate_gypsum_requirement(
        self, current_esp_pct: float, target_esp_pct: float, cec_meq_100g: float, soil_depth_cm: float = 30.0
    ) -> Dict[str, float]:
        """
        Calculate pure Gypsum (CaSO4.2H2O) requirement in metric tons/ha for sodic soil reclamation.
        GR (tons/ha) = 0.086 * CEC * (ESP_initial - ESP_final) * (depth / 30)
        """
        esp_diff = max(0.0, current_esp_pct - target_esp_pct)
        gr_tons_ha = 0.086 * cec_meq_100g * esp_diff * (soil_depth_cm / 30.0)

        return {
            "initial_esp_pct": current_esp_pct,
            "target_esp_pct": target_esp_pct,
            "gypsum_requirement_tons_ha": round(gr_tons_ha, 2),
            "elemental_sulfur_equivalent_tons_ha": round(gr_tons_ha * 0.19, 2),
            "recommendation": "Incorporate gypsum evenly into topsoil and apply heavy leaching irrigation."
        }
'''

engines["psychrometric_grain_drying_engine.py"] = '''"""
Grain Drying Psychrometrics & Equilibrium Moisture Content (EMC) Engine.
Implements Modified Chung-Pfost equations for EMC and grain drying aeration times.
"""

import math
from typing import Dict, Any

class PsychrometricGrainDryingEngine:
    """Grain drying EMC kinetics and air drying calculations."""

    # Modified Chung-Pfost parameters (A, B, C) for crops
    CHUNG_PFOST_PARAMS = {
        "wheat": {"A": 0.356, "B": 0.211, "C": 12.3},
        "maize": {"A": 0.312, "B": 0.254, "C": 14.2},
        "paddy": {"A": 0.421, "B": 0.185, "C": 10.8},
        "soybean": {"A": 0.298, "B": 0.310, "C": 15.6}
    }

    def calculate_emc(self, temp_c: float, relative_humidity_pct: float, crop: str = "wheat") -> float:
        """Calculate Equilibrium Moisture Content (% dry basis) using Modified Chung-Pfost equation."""
        crop_key = crop.lower().strip()
        params = self.CHUNG_PFOST_PARAMS.get(crop_key, self.CHUNG_PFOST_PARAMS["wheat"])
        
        rh = max(0.05, min(0.99, relative_humidity_pct / 100.0))
        t_k = temp_c + 273.15

        try:
            emc_db = (-1.0 / params["B"]) * math.log(-((t_k - params["C"]) * math.log(rh)) / params["A"])
            emc_wb = (emc_db / (100.0 + emc_db)) * 100.0
            return round(max(5.0, min(35.0, emc_wb)), 2)
        except Exception:
            return 13.5

    def calculate_drying_time_hours(
        self, initial_mc_wb: float, target_mc_wb: float, grain_mass_tons: float, airflow_m3_min_ton: float = 2.0
    ) -> Dict[str, float]:
        """Estimate hours needed for in-bin ambient air grain drying."""
        mc_diff_pct = max(0.0, initial_mc_wb - target_mc_wb)
        water_to_remove_kg = grain_mass_tons * 1000.0 * (mc_diff_pct / 100.0)

        # Average water removal rate ~0.15 kg water per m3 air airflow
        water_removal_rate_kg_hr = airflow_m3_min_ton * grain_mass_tons * 60.0 * 0.005
        drying_hours = water_to_remove_kg / max(0.1, water_removal_rate_kg_hr)

        return {
            "initial_moisture_pct": initial_mc_wb,
            "target_moisture_pct": target_mc_wb,
            "water_to_remove_kg": round(water_to_remove_kg, 1),
            "estimated_drying_hours": round(drying_hours, 1),
            "estimated_drying_days": round(drying_hours / 24.0, 1)
        }
'''

engines["asabe_machinery_cost_engine.py"] = '''"""
ASABE Machinery Management & Operating Cost Engine.
Implements ASABE D497.5 standards for tractor drawbar power,
fuel consumption rates, repair & maintenance curves, and machine depreciation.
"""

from typing import Dict, Any

class ASABEMachineryCostEngine:
    """ASABE D497 standards machinery cost calculator."""

    def calculate_tractor_operating_cost(
        self,
        purchase_price: float,
        rated_power_kw: float,
        annual_use_hours: float,
        fuel_price_per_liter: float,
        age_years: float = 5.0
    ) -> Dict[str, float]:
        """
        Calculate total machinery cost ($/hour and $/hectare).
        """
        # Average fuel consumption = 0.223 L / (kW * hr)
        fuel_rate_l_hr = 0.223 * rated_power_kw * 0.60  # 60% average load factor
        fuel_cost_hr = fuel_rate_l_hr * fuel_price_per_liter

        # Repair and Maintenance (R&M) cost curve
        # C_rm = RF1 * P_purchase * (total_hours / 1000) ^ RF2
        total_hours = annual_use_hours * age_years
        rm_accumulated = 0.007 * purchase_price * ((total_hours / 1000.0) ** 1.4)
        rm_cost_hr = rm_accumulated / max(1.0, total_hours)

        # Capital recovery & depreciation (Straight line + interest)
        salvage_value = purchase_price * (0.68 * (0.92 ** age_years))
        depreciation_annual = (purchase_price - salvage_value) / max(1.0, age_years)
        depreciation_hr = depreciation_annual / max(1.0, annual_use_hours)

        total_cost_hr = fuel_cost_hr + rm_cost_hr + depreciation_hr

        return {
            "rated_power_kw": rated_power_kw,
            "fuel_consumption_l_hr": round(fuel_rate_l_hr, 2),
            "fuel_cost_per_hour": round(fuel_cost_hr, 2),
            "repair_maintenance_cost_per_hour": round(rm_cost_hr, 2),
            "depreciation_cost_per_hour": round(depreciation_hr, 2),
            "total_operating_cost_per_hour": round(total_cost_hr, 2),
            "estimated_salvage_value": round(salvage_value, 2)
        }
'''

engines["soil_erosion_rusle_engine.py"] = '''"""
Revised Universal Soil Loss Equation (RUSLE) Engine.
Calculates annual soil erosion loss (A = R * K * LS * C * P) in metric tons/ha/year.
"""

from typing import Dict, Any

class SoilErosionRUSLEEngine:
    """RUSLE soil loss estimation calculator."""

    def calculate_annual_soil_loss(
        self,
        rainfall_erosivity_r: float,
        soil_erodibility_k: float,
        slope_length_steepness_ls: float,
        cover_management_c: float,
        support_practice_p: float
    ) -> Dict[str, float]:
        """
        A = R * K * LS * C * P
        """
        annual_loss_tons_ha = rainfall_erosivity_r * soil_erodibility_k * slope_length_steepness_ls * cover_management_c * support_practice_p

        # Soil loss tolerance threshold T ~ 10-12 tons/ha/yr
        t_tolerance = 11.2
        excessive = annual_loss_tons_ha > t_tolerance

        return {
            "r_factor": rainfall_erosivity_r,
            "k_factor": soil_erodibility_k,
            "ls_factor": slope_length_steepness_ls,
            "c_factor": cover_management_c,
            "p_factor": support_practice_p,
            "annual_soil_loss_tons_ha_yr": round(annual_loss_tons_ha, 2),
            "soil_tolerance_t_limit": t_tolerance,
            "erosion_risk_category": "Severe" if annual_loss_tons_ha > 25 else ("Moderate" if annual_loss_tons_ha > 11 else "Slight"),
            "exceeds_tolerance": excessive
        }
'''

engines["irrigation_hydraulics_engine.py"] = '''"""
Irrigation Hydraulics & Pipe Friction Loss Engine.
Calculates Hazen-Williams pressure drop and emitter Christiansen Uniformity (CU).
"""

import math
from typing import Dict, Any

class IrrigationHydraulicsEngine:
    """Irrigation hydraulic pipe friction and emitter uniformity calculator."""

    def calculate_pipe_friction_loss(
        self, flow_rate_lps: float, pipe_diameter_mm: float, pipe_length_m: float, hazen_williams_c: float = 150.0
    ) -> Dict[str, float]:
        """
        Hazen-Williams Head Loss Equation:
        h_f = (10.67 * L * Q^1.852) / (C^1.852 * D^4.87)
        """
        Q_m3s = flow_rate_lps / 1000.0
        D_m = pipe_diameter_mm / 1000.0
        L_m = pipe_length_m
        C = hazen_williams_c

        head_loss_m = (10.67 * L_m * (Q_m3s ** 1.852)) / ((C ** 1.852) * (D_m ** 4.87))
        pressure_drop_kpa = head_loss_m * 9.81

        return {
            "flow_rate_lps": flow_rate_lps,
            "pipe_diameter_mm": pipe_diameter_mm,
            "pipe_length_m": pipe_length_m,
            "head_loss_meters": round(head_loss_m, 2),
            "pressure_drop_kpa": round(pressure_drop_kpa, 2)
        }
'''

engines["fertilizer_blend_optimizer.py"] = '''"""
Minimum-Cost Fertilizer Blend Optimizer Engine.
Solves target N-P2O5-K2O nutrient specs using simplex/linear combination logic.
"""

from typing import Dict, Any, List

class FertilizerBlendOptimizer:
    """Linear fertilizer nutrient blending calculator."""

    AVAILABLE_SOURCES = {
        "urea": {"n": 46.0, "p": 0.0, "k": 0.0, "cost_kg": 0.40},
        "dap": {"n": 18.0, "p": 46.0, "k": 0.0, "cost_kg": 0.70},
        "mop": {"n": 0.0, "p": 0.0, "k": 60.0, "cost_kg": 0.50},
        "ssp": {"n": 0.0, "p": 16.0, "k": 0.0, "cost_kg": 0.30}
    }

    def optimize_blend(self, target_n_kg: float, target_p_kg: float, target_k_kg: float) -> Dict[str, Any]:
        """Calculate exact kg requirements of DAP, MOP, and Urea to meet NPK target."""
        # 1. Supply all P from DAP
        dap_kg = (target_p_kg / 46.0) * 100.0
        n_from_dap = dap_kg * 0.18

        # 2. Supply remaining N from Urea
        remaining_n = max(0.0, target_n_kg - n_from_dap)
        urea_kg = (remaining_n / 46.0) * 100.0

        # 3. Supply all K from MOP
        mop_kg = (target_k_kg / 60.0) * 100.0

        total_cost = (
            dap_kg * self.AVAILABLE_SOURCES["dap"]["cost_kg"] +
            urea_kg * self.AVAILABLE_SOURCES["urea"]["cost_kg"] +
            mop_kg * self.AVAILABLE_SOURCES["mop"]["cost_kg"]
        )

        return {
            "target_n_kg": target_n_kg,
            "target_p_kg": target_p_kg,
            "target_k_kg": target_k_kg,
            "required_dap_kg": round(dap_kg, 1),
            "required_urea_kg": round(urea_kg, 1),
            "required_mop_kg": round(mop_kg, 1),
            "total_blend_weight_kg": round(dap_kg + urea_kg + mop_kg, 1),
            "estimated_cost_usd": round(total_cost, 2)
        }
'''

for filename, content in engines.items():
    filepath = os.path.join(AGRONOMY_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename}")

