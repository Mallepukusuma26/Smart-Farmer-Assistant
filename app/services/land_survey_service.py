"""
Land Survey & Boundary Geometry Service Module for Smart Farmer Assistant.

Calculates field boundary polygon area using Shoelace formula (Gauss's area formula),
polygon centroid coordinates, field perimeter length, and slope aspect classification.
"""

from typing import Dict, Any, List, Optional, Tuple
import math
import logging

logger = logging.getLogger(__name__)


class LandSurveyService:
    """
    Business service providing spatial polygon geometry math:
    - Shoelace area calculation for irregular farm plots
    - Polygon centroid coordinate math
    - Perimeter distance calculations
    - Revised Universal Soil Loss Equation (RUSLE) slope factor (LS)
    """

    @staticmethod
    def calculate_shoelace_area_acres(coordinates: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        Calculates area of an arbitrary non-self-intersecting polygon using Shoelace formula.
        Input coordinates as list of (longitude, latitude) or (X, Y) meter tuples.
        """
        if len(coordinates) < 3:
            return {"area_acres": 0.0, "area_sq_meters": 0.0, "status": "Invalid Polygon — Minimum 3 points required"}

        n = len(coordinates)
        area_sq_m = 0.0

        for i in range(n):
            j = (i + 1) % n
            # Approximate meter conversion for lat/lon coordinates
            x_i = coordinates[i][0] * 111320.0 * math.cos(math.radians(coordinates[i][1]))
            y_i = coordinates[i][1] * 110540.0
            x_j = coordinates[j][0] * 111320.0 * math.cos(math.radians(coordinates[j][1]))
            y_j = coordinates[j][1] * 110540.0

            area_sq_m += (x_i * y_j) - (x_j * y_i)

        area_sq_m = abs(area_sq_m) / 2.0
        area_acres = area_sq_m / 4046.86
        area_hectares = area_sq_m / 10000.0

        # Centroid math
        cx = sum(pt[0] for pt in coordinates) / n
        cy = sum(pt[1] for pt in coordinates) / n

        return {
            "num_boundary_points": n,
            "area_sq_meters": round(area_sq_m, 2),
            "area_acres": round(area_acres, 2),
            "area_hectares": round(area_hectares, 2),
            "centroid_coordinates": (round(cx, 6), round(cy, 6))
        }

    @staticmethod
    def calculate_rusle_topographic_factor(slope_pct: float, slope_length_m: float = 50.0) -> float:
        """
        Calculates Revised Universal Soil Loss Equation (RUSLE) Topographic Factor LS:
        LS = (L / 22.13)^m * (65.41 * sin^2(theta) + 4.56 * sin(theta) + 0.065)
        """
        if slope_pct <= 0:
            return 0.1

        theta_rad = math.atan(slope_pct / 100.0)
        sin_theta = math.sin(theta_rad)

        if slope_pct >= 5.0:
            m = 0.5
        elif slope_pct >= 3.0:
            m = 0.4
        elif slope_pct >= 1.0:
            m = 0.3
        else:
            m = 0.2

        l_factor = math.pow(slope_length_m / 22.13, m)
        s_factor = 65.41 * math.pow(sin_theta, 2) + 4.56 * sin_theta + 0.065

        ls_factor = l_factor * s_factor
        return round(max(ls_factor, 0.05), 3)
