import os

extra_modules = [
    ("agronomy_grain_filling_duration.py", '''"""
Agronomy Grain Filling Duration Model for Smart Farmer Assistant.

Estimates grain filling phase duration based on thermal time, temperature stress, and soil moisture.
"""
from typing import Dict, Any

class AgronomyGrainFillingDurationEngine:
    @staticmethod
    def calculate_grain_filling_period(base_temp_c: float, max_temp_c: float, gdd_required: float, avg_daily_temp: float, moisture_stress_factor: float = 1.0) -> Dict[str, Any]:
        daily_gdd = max(0.0, avg_daily_temp - base_temp_c)
        if max_temp_c > 35.0:
            daily_gdd *= 0.85
        daily_gdd *= max(0.5, min(1.0, moisture_stress_factor))
        if daily_gdd <= 0:
            estimated_days = 999.0
        else:
            estimated_days = round(gdd_required / daily_gdd, 1)
        return {
            'daily_gdd': round(daily_gdd, 2),
            'estimated_grain_filling_days': estimated_days,
            'moisture_stress_applied': moisture_stress_factor < 0.8,
            'heat_stress_detected': max_temp_c > 35.0
        }
'''),
    ("agronomy_soil_compaction_index.py", '''"""
Agronomy Soil Compaction Index Engine for Smart Farmer Assistant.

Evaluates soil bulk density and penetrometer resistance to assess root growth restriction risks.
"""
from typing import Dict, Any

class AgronomySoilCompactionIndexEngine:
    @staticmethod
    def assess_compaction(bulk_density_g_cm3: float, soil_texture: str, cone_penetrometer_psi: float) -> Dict[str, Any]:
        critical_density = 1.65 if 'clay' in soil_texture.lower() else 1.80
        compaction_risk = 'Low'
        if bulk_density_g_cm3 >= critical_density or cone_penetrometer_psi > 300:
            compaction_risk = 'High'
        elif bulk_density_g_cm3 >= (critical_density - 0.15) or cone_penetrometer_psi > 200:
            compaction_risk = 'Moderate'
        return {
            'bulk_density_g_cm3': bulk_density_g_cm3,
            'critical_density_threshold': critical_density,
            'penetrometer_psi': cone_penetrometer_psi,
            'compaction_risk_level': compaction_risk,
            'recommendation': 'Subsoiling / deep tillage required' if compaction_risk == 'High' else 'Standard tillage practices'
        }
'''),
    ("agronomy_canopy_extinction_coefficient.py", '''"""
Agronomy Canopy Light Extinction Coefficient Engine for Smart Farmer Assistant.

Calculates PAR attenuation through the crop canopy using Beer-Lambert law.
"""
import math
from typing import Dict, Any

class AgronomyCanopyExtinctionCoefficientEngine:
    @staticmethod
    def calculate_par_interception(leaf_area_index: float, extinction_k: float = 0.65, incident_par_mj_m2: float = 20.0) -> Dict[str, Any]:
        interception_fraction = 1.0 - math.exp(-extinction_k * leaf_area_index)
        intercepted_par = round(incident_par_mj_m2 * interception_fraction, 2)
        transmitted_par = round(incident_par_mj_m2 - intercepted_par, 2)
        return {
            'leaf_area_index': leaf_area_index,
            'extinction_k': extinction_k,
            'interception_fraction_pct': round(interception_fraction * 100, 1),
            'intercepted_par_mj_m2': intercepted_par,
            'transmitted_par_mj_m2': transmitted_par
        }
'''),
    ("agronomy_nitrogen_leaching_loss.py", '''"""
Agronomy Nitrogen Leaching Loss Engine for Smart Farmer Assistant.

Estimates nitrate leaching potential based on rainfall, soil drainage, and soil N pool.
"""
from typing import Dict, Any

class AgronomyNitrogenLeachingLossEngine:
    @staticmethod
    def estimate_n_leaching(applied_n_kg_ha: float, rainfall_mm: float, drainage_capacity: str, soil_sand_pct: float) -> Dict[str, Any]:
        leaching_coeff = 0.05
        if soil_sand_pct > 60:
            leaching_coeff += 0.15
        if drainage_capacity.lower() in ['excessive', 'high']:
            leaching_coeff += 0.10
        if rainfall_mm > 100:
            leaching_coeff += (rainfall_mm - 100) * 0.002
        leaching_coeff = min(0.60, max(0.02, leaching_coeff))
        estimated_n_lost_kg_ha = round(applied_n_kg_ha * leaching_coeff, 2)
        return {
            'applied_n_kg_ha': applied_n_kg_ha,
            'leaching_coefficient': round(leaching_coeff, 3),
            'estimated_n_lost_kg_ha': estimated_n_lost_kg_ha,
            'retained_n_kg_ha': round(applied_n_kg_ha - estimated_n_lost_kg_ha, 2),
            'mitigation_advice': 'Split application of nitrogen recommended' if leaching_coeff > 0.25 else 'Standard nitrogen management adequate'
        }
'''),
    ("agronomy_crop_water_productivity.py", '''"""
Agronomy Crop Water Productivity (CWP) Engine for Smart Farmer Assistant.

Calculates yield per unit of evapotranspired water (kg/m3).
"""
from typing import Dict, Any

class AgronomyCropWaterProductivityEngine:
    @staticmethod
    def calculate_cwp(yield_kg_ha: float, total_evapotranspiration_mm: float) -> Dict[str, Any]:
        water_volume_m3 = total_evapotranspiration_mm * 10.0
        if water_volume_m3 <= 0:
            cwp_kg_m3 = 0.0
        else:
            cwp_kg_m3 = round(yield_kg_ha / water_volume_m3, 3)
        return {
            'yield_kg_ha': yield_kg_ha,
            'evapotranspiration_mm': total_evapotranspiration_mm,
            'water_volume_m3_ha': water_volume_m3,
            'crop_water_productivity_kg_m3': cwp_kg_m3,
            'benchmarking': 'High Efficiency' if cwp_kg_m3 >= 1.5 else 'Average Efficiency' if cwp_kg_m3 >= 0.8 else 'Needs Improvement'
        }
'''),
    ("agronomy_radiation_use_efficiency.py", '''"""
Agronomy Radiation Use Efficiency (RUE) Engine for Smart Farmer Assistant.

Calculates biomass accumulation per unit of intercepted solar radiation (g/MJ).
"""
from typing import Dict, Any

class AgronomyRadiationUseEfficiencyEngine:
    @staticmethod
    def calculate_biomass_production(intercepted_solar_rad_mj_m2: float, rue_g_mj: float = 1.45, stress_factor: float = 1.0) -> Dict[str, Any]:
        actual_rue = rue_g_mj * min(1.0, max(0.2, stress_factor))
        produced_biomass_g_m2 = round(intercepted_solar_rad_mj_m2 * actual_rue, 2)
        produced_biomass_kg_ha = round(produced_biomass_g_m2 * 10.0, 1)
        return {
            'potential_rue_g_mj': rue_g_mj,
            'actual_rue_g_mj': round(actual_rue, 3),
            'biomass_g_m2': produced_biomass_g_m2,
            'biomass_kg_ha': produced_biomass_kg_ha,
            'stress_penalty_pct': round((1.0 - stress_factor) * 100, 1)
        }
'''),
    ("agronomy_drought_susceptibility_index.py", '''"""
Agronomy Drought Susceptibility Index (DSI) Engine for Smart Farmer Assistant.

Quantifies crop yield stability under water deficit conditions.
"""
from typing import Dict, Any

class AgronomyDroughtSusceptibilityIndexEngine:
    @staticmethod
    def calculate_dsi(yield_stress: float, yield_potential: float, mean_yield_stress_all: float, mean_yield_potential_all: float) -> Dict[str, Any]:
        if yield_potential <= 0 or mean_yield_potential_all <= 0:
            return {'error': 'Invalid yield values for DSI calculation'}
        stress_intensity = 1.0 - (mean_yield_stress_all / mean_yield_potential_all)
        if stress_intensity <= 0:
            dsi = 0.0
        else:
            dsi = round((1.0 - (yield_stress / yield_potential)) / stress_intensity, 3)
        tolerance_category = 'Highly Tolerant' if dsi < 0.5 else 'Moderately Tolerant' if dsi <= 1.0 else 'Susceptible'
        return {
            'yield_stress': yield_stress,
            'yield_potential': yield_potential,
            'drought_susceptibility_index': dsi,
            'tolerance_category': tolerance_category
        }
'''),
    ("agronomy_field_trafficability_assessment.py", '''"""
Agronomy Field Trafficability Engine for Smart Farmer Assistant.

Assesses soil moisture and bearing capacity for machinery field operations.
"""
from typing import Dict, Any

class AgronomyFieldTrafficabilityEngine:
    @staticmethod
    def assess_trafficability(soil_moisture_pct: float, field_capacity_pct: float, clay_pct: float) -> Dict[str, Any]:
        relative_moisture = soil_moisture_pct / max(1.0, field_capacity_pct)
        trafficable = True
        risk_level = 'Low'
        if relative_moisture > 0.95:
            trafficable = False
            risk_level = 'Severe Rutting and Compaction Risk'
        elif relative_moisture > 0.85:
            trafficable = True
            risk_level = 'Moderate Compaction Risk'
        return {
            'soil_moisture_pct': soil_moisture_pct,
            'field_capacity_pct': field_capacity_pct,
            'relative_moisture': round(relative_moisture, 2),
            'trafficable': trafficable,
            'compaction_risk': risk_level,
            'recommendation': 'Proceed with field machinery' if trafficable and relative_moisture <= 0.85 else 'Delay heavy field operations to avoid subsoil compaction'
        }
'''),
    ("agronomy_phosphorus_fixation_index.py", '''"""
Agronomy Phosphorus Fixation Index Engine for Smart Farmer Assistant.

Predicts soil P-binding capacity based on pH, clay content, and organic matter.
"""
from typing import Dict, Any

class AgronomyPhosphorusFixationIndexEngine:
    @staticmethod
    def calculate_p_fixation(soil_ph: float, clay_pct: float, organic_matter_pct: float) -> Dict[str, Any]:
        fixation_score = clay_pct * 0.8
        if soil_ph < 5.5:
            fixation_score += (5.5 - soil_ph) * 15.0
        elif soil_ph > 7.8:
            fixation_score += (soil_ph - 7.8) * 12.0
        fixation_score -= organic_matter_pct * 3.0
        fixation_score = max(0.0, min(100.0, fixation_score))
        availability_factor = round(1.0 - (fixation_score / 100.0 * 0.7), 2)
        return {
            'soil_ph': soil_ph,
            'clay_pct': clay_pct,
            'p_fixation_score': round(fixation_score, 1),
            'p_availability_factor': availability_factor,
            'management_tip': 'Apply mycorrhizal inoculants or band-apply P fertilizer' if fixation_score > 60 else 'Standard broadcast application acceptable'
        }
'''),
    ("agronomy_potassium_release_dynamics.py", '''"""
Agronomy Potassium Release Dynamics Engine for Smart Farmer Assistant.

Models exchangeable vs non-exchangeable K release rates in clay-rich soils.
"""
from typing import Dict, Any

class AgronomyPotassiumReleaseDynamicsEngine:
    @staticmethod
    def calculate_k_buffer_capacity(exchangeable_k_ppm: float, illite_clay_pct: float) -> Dict[str, Any]:
        buffering_capacity = exchangeable_k_ppm * (1.0 + (illite_clay_pct * 0.03))
        release_rate_kg_ha_day = round(buffering_capacity * 0.005, 2)
        return {
            'exchangeable_k_ppm': exchangeable_k_ppm,
            'illite_clay_pct': illite_clay_pct,
            'k_buffering_index': round(buffering_capacity, 1),
            'estimated_daily_k_release_kg_ha': release_rate_kg_ha_day,
            'k_sufficiency_status': 'Sufficient' if exchangeable_k_ppm >= 120 else 'Deficient'
        }
'''),
    ("agronomy_soil_microbial_respiration.py", '''"""
Agronomy Soil Microbial Respiration Engine for Smart Farmer Assistant.

Estimates soil biological activity (CO2 efflux) based on temperature and moisture.
"""
import math
from typing import Dict, Any

class AgronomySoilMicrobialRespirationEngine:
    @staticmethod
    def estimate_co2_efflux(soil_temp_c: float, soil_moisture_vwc: float, organic_carbon_pct: float) -> Dict[str, Any]:
        q10 = 2.0
        base_resp = organic_carbon_pct * 1.2
        temp_factor = math.pow(q10, (soil_temp_c - 20.0) / 10.0)
        moisture_factor = min(1.0, max(0.1, soil_moisture_vwc / 0.35))
        co2_efflux_mg_kg_day = round(base_resp * temp_factor * moisture_factor, 2)
        return {
            'soil_temp_c': soil_temp_c,
            'soil_moisture_vwc': soil_moisture_vwc,
            'organic_carbon_pct': organic_carbon_pct,
            'co2_efflux_mg_kg_day': co2_efflux_mg_kg_day,
            'biological_activity_level': 'High' if co2_efflux_mg_kg_day > 15.0 else 'Moderate' if co2_efflux_mg_kg_day > 5.0 else 'Low'
        }
'''),
    ("agronomy_yield_gap_analysis.py", '''"""
Agronomy Yield Gap Analysis Engine for Smart Farmer Assistant.

Computes potential yield, water-limited yield, and actual yield gaps for crops.
"""
from typing import Dict, Any

class AgronomyYieldGapAnalysisEngine:
    @staticmethod
    def analyze_yield_gap(potential_yield_t_ha: float, actual_yield_t_ha: float) -> Dict[str, Any]:
        yield_gap_t_ha = round(potential_yield_t_ha - actual_yield_t_ha, 2)
        exploitation_rate_pct = round((actual_yield_t_ha / max(0.1, potential_yield_t_ha)) * 100, 1)
        return {
            'potential_yield_t_ha': potential_yield_t_ha,
            'actual_yield_t_ha': actual_yield_t_ha,
            'yield_gap_t_ha': yield_gap_t_ha,
            'exploitation_rate_pct': exploitation_rate_pct,
            'closing_gap_priority': 'High' if exploitation_rate_pct < 70 else 'Medium' if exploitation_rate_pct < 85 else 'Low'
        }
'''),
    ("agronomy_leaf_senescence_model.py", '''"""
Agronomy Leaf Senescence Engine for Smart Farmer Assistant.

Models accelerated leaf area loss due to drought, nitrogen deficit, and natural aging.
"""
from typing import Dict, Any

class AgronomyLeafSenescenceModelEngine:
    @staticmethod
    def calculate_senescence_rate(current_lai: float, days_after_anthesis: int, nitrogen_stress_factor: float = 1.0, water_stress_factor: float = 1.0) -> Dict[str, Any]:
        base_senescence = 0.02 * (days_after_anthesis / 30.0)
        accelerated_senescence = base_senescence * (2.0 - nitrogen_stress_factor) * (2.0 - water_stress_factor)
        new_lai = max(0.0, round(current_lai - accelerated_senescence, 2))
        return {
            'current_lai': current_lai,
            'days_after_anthesis': days_after_anthesis,
            'daily_lai_loss': round(accelerated_senescence, 3),
            'updated_lai': new_lai,
            'senescence_stage': 'Rapid Senescence' if accelerated_senescence > 0.08 else 'Normal Senescence'
        }
'''),
    ("agronomy_precision_fertigation_calculator.py", '''"""
Agronomy Precision Fertigation Calculator Engine for Smart Farmer Assistant.

Calculates nutrient injection rates for drip fertigation systems.
"""
from typing import Dict, Any

class AgronomyPrecisionFertigationCalculatorEngine:
    @staticmethod
    def calculate_injection_rate(target_n_ppm: float, irrigation_flow_rate_lph: float, fertilizer_n_pct: float = 19.0) -> Dict[str, Any]:
        fertilizer_concentration = fertilizer_n_pct * 10000.0
        injection_rate_lph = round((target_n_ppm * irrigation_flow_rate_lph) / max(1.0, fertilizer_concentration), 2)
        return {
            'target_n_ppm': target_n_ppm,
            'irrigation_flow_rate_lph': irrigation_flow_rate_lph,
            'fertilizer_n_pct': fertilizer_n_pct,
            'injection_rate_lph': injection_rate_lph,
            'dilution_ratio': f'1:{int(irrigation_flow_rate_lph / max(0.01, injection_rate_lph))}'
        }
'''),
    ("agronomy_solar_irradiance_calculator.py", '''"""
Agronomy Solar Irradiance Calculator Engine for Smart Farmer Assistant.

Calculates clear-sky solar irradiance and photoperiod for crop growth modeling.
"""
import math
from typing import Dict, Any

class AgronomySolarIrradianceCalculatorEngine:
    @staticmethod
    def calculate_daily_extraterrestrial_radiation(latitude_deg: float, day_of_year: int) -> Dict[str, Any]:
        lat_rad = math.radians(latitude_deg)
        declination = 0.409 * math.sin((2 * math.pi / 365 * day_of_year) - 1.39)
        ws = math.acos(-math.tan(lat_rad) * math.tan(declination))
        dr = 1 + 0.033 * math.cos(2 * math.pi / 365 * day_of_year)
        ra = (24 * 60 / math.pi) * 0.0820 * dr * (ws * math.sin(lat_rad) * math.sin(declination) + math.cos(lat_rad) * math.cos(declination) * math.sin(ws))
        day_length_hours = round(2 * ws * 24 / (2 * math.pi), 1)
        return {
            'latitude_deg': latitude_deg,
            'day_of_year': day_of_year,
            'extraterrestrial_radiation_mj_m2_day': round(ra, 2),
            'day_length_hours': day_length_hours
        }
''')
]

target_dir = 'app/services/agronomy'
for fname, content in extra_modules:
    fpath = os.path.join(target_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print(f'Successfully wrote {len(extra_modules)} modules.')
