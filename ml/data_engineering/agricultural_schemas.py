"""
Agricultural Data Schemas Module for Smart Farmer Assistant.

Defines dataclasses and validation rules for ML input/output data structures:
CropInput, YieldInput, DiseaseImageFeatures, FertilizerInput, and ProfitInput.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class CropInputSchema:
    """
    Input schema for crop recommendation engine.
    """
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

    def validate(self) -> List[str]:
        errors = []
        if not (0 <= self.N <= 300):
            errors.append("Nitrogen (N) must be between 0 and 300 mg/kg")
        if not (0 <= self.P <= 300):
            errors.append("Phosphorus (P) must be between 0 and 300 mg/kg")
        if not (0 <= self.K <= 300):
            errors.append("Potassium (K) must be between 0 and 300 mg/kg")
        if not (-10 <= self.temperature <= 60):
            errors.append("Temperature must be between -10°C and 60°C")
        if not (0 <= self.humidity <= 100):
            errors.append("Humidity must be between 0% and 100%")
        if not (0 <= self.ph <= 14):
            errors.append("pH must be between 0 and 14")
        if not (0 <= self.rainfall <= 3000):
            errors.append("Rainfall must be between 0 and 3000 mm")
        return errors


@dataclass
class YieldInputSchema:
    """
    Input schema for crop yield prediction regressor.
    """
    crop_name: str
    rainfall_mm: float
    pesticides_tonnes: float
    avg_temp: float
    area_acres: float = 1.0

    def validate(self) -> List[str]:
        errors = []
        if not self.crop_name:
            errors.append("Crop name is required")
        if self.rainfall_mm < 0:
            errors.append("Rainfall cannot be negative")
        if self.pesticides_tonnes < 0:
            errors.append("Pesticides quantity cannot be negative")
        if self.area_acres <= 0:
            errors.append("Area in acres must be greater than 0")
        return errors


@dataclass
class DiseaseFeatureSchema:
    """
    Extracted computer vision features schema for plant leaf image diagnosis.
    """
    mean_r: float
    mean_g: float
    mean_b: float
    mean_h: float
    mean_s: float
    mean_v: float
    std_r: float
    std_g: float
    std_b: float
    glcm_contrast: float
    glcm_homogeneity: float
    glcm_energy: float
    sobel_edge_density: float
    hu_moment_1: float
    hu_moment_2: float


@dataclass
class ProfitInputSchema:
    """
    Input schema for farm profitability predictor.
    """
    crop_name: str
    total_investment: float
    land_area_acres: float
    expected_yield_per_acre: float
    market_price: float

    def validate(self) -> List[str]:
        errors = []
        if self.total_investment < 0:
            errors.append("Total investment cannot be negative")
        if self.land_area_acres <= 0:
            errors.append("Land area must be greater than 0")
        if self.expected_yield_per_acre < 0:
            errors.append("Expected yield cannot be negative")
        if self.market_price < 0:
            errors.append("Market price cannot be negative")
        return errors
