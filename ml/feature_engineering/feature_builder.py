import numpy as np

def compute_npk_ratios(n, p, k):
    """Compute NPK ratio balance metrics."""
    total = max(n + p + k, 1.0)
    return {
        'n_ratio': round(n / total, 3),
        'p_ratio': round(p / total, 3),
        'k_ratio': round(k / total, 3),
        'npk_total': round(total, 2)
    }

def compute_temperature_humidity_index(temperature, humidity):
    """Calculate agro-climatic Temperature-Humidity Index (THI)."""
    return round(temperature - (0.55 - 0.0055 * humidity) * (temperature - 14.5), 2)

def compute_soil_health_score(ph, n, p, k, organic_carbon, ec):
    """Algorithmic Soil Health Score calculation (0 - 100 scale)."""
    score = 100.0
    
    # pH penalty (ideal 6.0 - 7.5)
    if ph < 6.0 or ph > 7.5:
        score -= abs(ph - 6.75) * 8.0
        
    # Nitrogen rating (ideal 100-250)
    if n < 80:
        score -= (80 - n) * 0.2
    elif n > 300:
        score -= (n - 300) * 0.1
        
    # Phosphorus rating (ideal 30-80)
    if p < 25:
        score -= (25 - p) * 0.3
        
    # Potassium rating (ideal 100-250)
    if k < 80:
        score -= (80 - k) * 0.15
        
    # Organic Carbon rating (ideal > 0.75%)
    if organic_carbon < 0.5:
        score -= (0.5 - organic_carbon) * 30.0
        
    # Electrical Conductivity (ideal < 1.5 dS/m)
    if ec > 1.5:
        score -= (ec - 1.5) * 15.0

    return max(10.0, min(100.0, round(score, 1)))
