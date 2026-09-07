import os

extra_modules_2 = [
    ("agronomy_root_respiration_engine.py", '''"""
Agronomy Root Respiration Engine for Smart Farmer Assistant.

Calculates root respiration rate and oxygen consumption based on soil temperature and porosity.
"""
from typing import Dict, Any

class AgronomyRootRespirationEngine:
    @staticmethod
    def calculate_root_respiration(root_mass_g_m2: float, soil_temp_c: float, oxygen_concentration_pct: float) -> Dict[str, Any]:
        temp_factor = 2.0 ** ((soil_temp_c - 20.0) / 10.0)
        o2_factor = max(0.1, min(1.0, oxygen_concentration_pct / 21.0))
        respiration_rate_mg_o2_m2_hr = round(root_mass_g_m2 * 0.15 * temp_factor * o2_factor, 2)
        return {
            'root_mass_g_m2': root_mass_g_m2,
            'soil_temp_c': soil_temp_c,
            'oxygen_concentration_pct': oxygen_concentration_pct,
            'respiration_rate_mg_o2_m2_hr': respiration_rate_mg_o2_m2_hr,
            'aeration_status': 'Optimal' if oxygen_concentration_pct > 15.0 else 'Hypoxic Risk'
        }
'''),
    ("agronomy_crop_salinity_tolerance.py", '''"""
Agronomy Crop Salinity Tolerance Engine for Smart Farmer Assistant.

Models Maas-Hoffman yield reduction function based on electrical conductivity (ECe).
"""
from typing import Dict, Any

class AgronomyCropSalinityToleranceEngine:
    @staticmethod
    def calculate_yield_reduction(ece_ds_m: float, threshold_ece: float = 1.7, slope_pct_per_ds_m: float = 12.0) -> Dict[str, Any]:
        if ece_ds_m <= threshold_ece:
            yield_loss_pct = 0.0
        else:
            yield_loss_pct = min(100.0, round((ece_ds_m - threshold_ece) * slope_pct_per_ds_m, 1))
        expected_yield_pct = round(100.0 - yield_loss_pct, 1)
        return {
            'ece_ds_m': ece_ds_m,
            'threshold_ece': threshold_ece,
            'yield_loss_pct': yield_loss_pct,
            'expected_yield_pct': expected_yield_pct,
            'salinity_hazard': 'Severe' if yield_loss_pct > 30 else 'Moderate' if yield_loss_pct > 10 else 'None'
        }
'''),
    ("agronomy_phosphorus_desorption_rate.py", '''"""
Agronomy Phosphorus Desorption Rate Engine for Smart Farmer Assistant.

Estimates P release kinetic parameters in weathered tropical soils.
"""
from typing import Dict, Any

class AgronomyPhosphorusDesorptionRateEngine:
    @staticmethod
    def estimate_desorption(labile_p_mg_kg: float, fe_ox_content_g_kg: float) -> Dict[str, Any]:
        desorption_constant = 0.045 / max(1.0, (fe_ox_content_g_kg * 0.1))
        daily_release_mg_kg = round(labile_p_mg_kg * desorption_constant, 3)
        return {
            'labile_p_mg_kg': labile_p_mg_kg,
            'fe_ox_content_g_kg': fe_ox_content_g_kg,
            'desorption_rate_constant': round(desorption_constant, 4),
            'daily_p_release_mg_kg': daily_release_mg_kg
        }
'''),
    ("agronomy_nitrogen_volatilization_risk.py", '''"""
Agronomy Nitrogen Volatilization Risk Engine for Smart Farmer Assistant.

Calculates ammonia volatilization from surface-applied urea under high pH and wind.
"""
from typing import Dict, Any

class AgronomyNitrogenVolatilizationRiskEngine:
    @staticmethod
    def assess_volatilization(surface_applied_urea_kg_ha: float, soil_ph: float, temp_c: float, wind_speed_m_s: float) -> Dict[str, Any]:
        risk_score = 0.0
        if soil_ph > 7.0:
            risk_score += (soil_ph - 7.0) * 20.0
        if temp_c > 25.0:
            risk_score += (temp_c - 25.0) * 1.5
        risk_score += wind_speed_m_s * 5.0
        loss_pct = min(45.0, max(2.0, risk_score * 0.5))
        loss_kg_n_ha = round(surface_applied_urea_kg_ha * 0.46 * (loss_pct / 100.0), 2)
        return {
            'applied_urea_kg_ha': surface_applied_urea_kg_ha,
            'soil_ph': soil_ph,
            'estimated_n_loss_pct': round(loss_pct, 1),
            'estimated_nh3_loss_kg_n_ha': loss_kg_n_ha,
            'mitigation_recommendation': 'Incorporate urea into top 5cm soil immediately or use urease inhibitor' if loss_pct > 15.0 else 'Low volatilization risk'
        }
'''),
    ("agronomy_canopy_temperatures_stress_index.py", '''"""
Agronomy Canopy Temperature Stress Index (CWSI) Engine for Smart Farmer Assistant.

Computes Crop Water Stress Index based on canopy and ambient air temperature difference.
"""
from typing import Dict, Any

class AgronomyCanopyTemperatureStressIndexEngine:
    @staticmethod
    def calculate_cwsi(tc_minus_ta: float, lower_baseline: float = -2.5, upper_baseline: float = 4.5) -> Dict[str, Any]:
        cwsi = (tc_minus_ta - lower_baseline) / max(0.1, (upper_baseline - lower_baseline))
        cwsi = min(1.0, max(0.0, round(cwsi, 2)))
        return {
            'canopy_air_temp_diff_c': tc_minus_ta,
            'cwsi': cwsi,
            'irrigation_urgency': 'Immediate Irrigation Required' if cwsi > 0.6 else 'Moderate Stress' if cwsi > 0.3 else 'Well Watered'
        }
'''),
    ("agronomy_soil_organic_matter_decomposition.py", '''"""
Agronomy Soil Organic Matter Decomposition Engine for Smart Farmer Assistant.

Calculates turnover rate of labile and recalcitrant organic carbon pools.
"""
from typing import Dict, Any

class AgronomySoilOrganicMatterDecompositionEngine:
    @staticmethod
    def calculate_som_turnover(total_soc_g_kg: float, c_n_ratio: float, clay_pct: float) -> Dict[str, Any]:
        k_decomp = 0.0008 * (30.0 / max(10.0, c_n_ratio)) * (1.0 - (clay_pct * 0.005))
        annual_humus_min_kg_ha = round(total_soc_g_kg * 2000.0 * k_decomp, 1)
        return {
            'total_soc_g_kg': total_soc_g_kg,
            'c_n_ratio': c_n_ratio,
            'clay_pct': clay_pct,
            'k_decomposition': round(k_decomp, 5),
            'annual_mineralized_n_kg_ha': round(annual_humus_min_kg_ha * 0.08, 1)
        }
'''),
    ("agronomy_vermicompost_application_rate.py", '''"""
Agronomy Vermicompost Application Rate Calculator Engine for Smart Farmer Assistant.

Determines optimal organic matter amendment rate based on target organic carbon increase.
"""
from typing import Dict, Any

class AgronomyVermicompostApplicationRateEngine:
    @staticmethod
    def calculate_vermicompost_requirement(current_soc_pct: float, target_soc_pct: float, soil_depth_cm: float = 15.0) -> Dict[str, Any]:
        soc_deficit_pct = max(0.0, target_soc_pct - current_soc_pct)
        soil_weight_ton_ha = 2250.0 * (soil_depth_cm / 15.0)
        soc_needed_ton_ha = soil_weight_ton_ha * (soc_deficit_pct / 100.0)
        vermicompost_ton_ha = round(soc_needed_ton_ha / 0.15, 2)
        return {
            'current_soc_pct': current_soc_pct,
            'target_soc_pct': target_soc_pct,
            'soc_needed_ton_ha': round(soc_needed_ton_ha, 2),
            'vermicompost_required_ton_ha': vermicompost_ton_ha,
            'application_method': 'Broadcast and incorporate prior to sowing'
        }
'''),
    ("agronomy_thermal_time_gdd_accumulator.py", '''"""
Agronomy Thermal Time Growing Degree Days (GDD) Accumulator Engine for Smart Farmer Assistant.

Calculates accumulated growing degree days for phenological stage transitions.
"""
from typing import List, Dict, Any

class AgronomyThermalTimeGDDAccumulatorEngine:
    @staticmethod
    def accumulate_gdd(daily_tmax: List[float], daily_tmin: List[float], t_base: float = 10.0, t_cutoff: float = 30.0) -> Dict[str, Any]:
        total_gdd = 0.0
        daily_records = []
        for tmax, tmin in zip(daily_tmax, daily_tmin):
            adj_max = min(t_cutoff, tmax)
            adj_min = max(t_base, tmin)
            t_avg = (adj_max + adj_min) / 2.0
            gdd = max(0.0, t_avg - t_base)
            total_gdd += gdd
            daily_records.append(round(gdd, 1))
        return {
            'days_count': len(daily_tmax),
            't_base': t_base,
            't_cutoff': t_cutoff,
            'total_accumulated_gdd': round(total_gdd, 1),
            'daily_gdd_series': daily_records
        }
'''),
    ("agronomy_crop_rotation_benefit_analyzer.py", '''"""
Agronomy Crop Rotation Benefit Analyzer Engine for Smart Farmer Assistant.

Quantifies yield advantage and pest break benefits of legume-cereal crop rotations.
"""
from typing import Dict, Any

class AgronomyCropRotationBenefitAnalyzerEngine:
    @staticmethod
    def analyze_rotation_benefit(previous_crop: str, current_crop: str) -> Dict[str, Any]:
        n_credit_kg_ha = 0.0
        yield_boost_pct = 0.0
        disease_break_score = 'Standard'

        prev = previous_crop.lower()
        curr = current_crop.lower()

        if any(legume in prev for legume in ['chickpea', 'pigeonpea', 'soybean', 'groundnut', 'lentil', 'cowpea']):
            n_credit_kg_ha = 30.0
            yield_boost_pct = 12.5
            disease_break_score = 'Excellent Disease/Pest Break'
        elif prev != curr:
            yield_boost_pct = 5.0
            disease_break_score = 'Moderate Break'

        return {
            'previous_crop': previous_crop,
            'current_crop': current_crop,
            'nitrogen_credit_kg_ha': n_credit_kg_ha,
            'expected_yield_boost_pct': yield_boost_pct,
            'disease_break_evaluation': disease_break_score
        }
'''),
    ("agronomy_potassium_fixation_capacity.py", '''"""
Agronomy Potassium Fixation Capacity Engine for Smart Farmer Assistant.

Estimates 2:1 clay mineral K-fixation risk in high pH soils.
"""
from typing import Dict, Any

class AgronomyPotassiumFixationCapacityEngine:
    @staticmethod
    def estimate_k_fixation(smectite_clay_pct: float, soil_ph: float) -> Dict[str, Any]:
        fixation_risk_pct = round(min(60.0, smectite_clay_pct * 0.9 + max(0.0, (soil_ph - 7.5) * 5.0)), 1)
        return {
            'smectite_clay_pct': smectite_clay_pct,
            'soil_ph': soil_ph,
            'k_fixation_risk_pct': fixation_risk_pct,
            'fertilizer_placement_advice': 'Band placement near root zone to minimize fixation' if fixation_risk_pct > 25.0 else 'Broadcast application acceptable'
        }
''')
]

target_dir = 'app/services/agronomy'
for fname, content in extra_modules_2:
    fpath = os.path.join(target_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print(f'Successfully wrote {len(extra_modules_2)} additional modules.')
