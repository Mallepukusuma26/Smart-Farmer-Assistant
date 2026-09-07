import os
import numpy as np
import pandas as pd

DATASET_DIR = os.path.join(os.path.dirname(__file__), 'datasets')
os.makedirs(DATASET_DIR, exist_ok=True)

def generate_crop_recommendation_dataset():
    """Generate realistic crop recommendation dataset (22 crops, 2200 samples)."""
    np.random.seed(42)
    crops_config = {
        'Rice': {'n': (60, 120), 'p': (35, 60), 'k': (35, 45), 'temp': (20, 27), 'hum': (80, 90), 'ph': (5.0, 6.5), 'rain': (180, 300)},
        'Maize': {'n': (60, 100), 'p': (35, 60), 'k': (15, 25), 'temp': (18, 27), 'hum': (55, 75), 'ph': (5.5, 7.0), 'rain': (60, 110)},
        'Chickpea': {'n': (20, 50), 'p': (55, 80), 'k': (75, 85), 'temp': (17, 21), 'hum': (14, 20), 'ph': (6.0, 8.5), 'rain': (65, 95)},
        'Kidneybeans': {'n': (15, 40), 'p': (55, 80), 'k': (15, 25), 'temp': (15, 25), 'hum': (18, 25), 'ph': (5.5, 6.0), 'rain': (60, 150)},
        'Pigeonpeas': {'n': (15, 40), 'p': (55, 80), 'k': (15, 25), 'temp': (27, 38), 'hum': (45, 65), 'ph': (4.5, 7.5), 'rain': (90, 200)},
        'Mothbeans': {'n': (15, 40), 'p': (35, 60), 'k': (15, 25), 'temp': (24, 32), 'hum': (40, 65), 'ph': (3.5, 10.0), 'rain': (30, 75)},
        'Mungbean': {'n': (15, 40), 'p': (35, 60), 'k': (15, 25), 'temp': (27, 30), 'hum': (80, 90), 'ph': (6.2, 7.2), 'rain': (35, 60)},
        'Blackgram': {'n': (35, 60), 'p': (55, 80), 'k': (15, 25), 'temp': (25, 35), 'hum': (60, 75), 'ph': (6.5, 7.5), 'rain': (60, 75)},
        'Lentil': {'n': (15, 40), 'p': (55, 80), 'k': (15, 25), 'temp': (18, 30), 'hum': (60, 70), 'ph': (5.9, 7.4), 'rain': (35, 55)},
        'Pomegranate': {'n': (15, 40), 'p': (10, 30), 'k': (35, 45), 'temp': (18, 25), 'hum': (85, 95), 'ph': (5.5, 7.2), 'rain': (100, 110)},
        'Banana': {'n': (90, 120), 'p': (70, 95), 'k': (45, 55), 'temp': (25, 30), 'hum': (75, 85), 'ph': (5.5, 6.5), 'rain': (90, 120)},
        'Mango': {'n': (15, 40), 'p': (15, 40), 'k': (25, 35), 'temp': (27, 36), 'hum': (48, 55), 'ph': (4.5, 7.0), 'rain': (90, 100)},
        'Grapes': {'n': (10, 40), 'p': (120, 145), 'k': (195, 205), 'temp': (8, 42), 'hum': (80, 85), 'ph': (5.5, 6.5), 'rain': (65, 75)},
        'Watermelon': {'n': (80, 120), 'p': (5, 30), 'k': (45, 55), 'temp': (24, 27), 'hum': (80, 90), 'ph': (6.0, 7.0), 'rain': (40, 60)},
        'Muskmelon': {'n': (80, 120), 'p': (5, 30), 'k': (45, 55), 'temp': (27, 29), 'hum': (90, 95), 'ph': (6.0, 6.8), 'rain': (20, 30)},
        'Apple': {'n': (15, 40), 'p': (120, 145), 'k': (195, 205), 'temp': (21, 24), 'hum': (90, 95), 'ph': (5.5, 6.5), 'rain': (100, 120)},
        'Orange': {'n': (15, 40), 'p': (10, 30), 'k': (5, 15), 'temp': (10, 35), 'hum': (90, 95), 'ph': (6.0, 7.5), 'rain': (100, 120)},
        'Papaya': {'n': (35, 70), 'p': (45, 70), 'k': (45, 55), 'temp': (23, 44), 'hum': (90, 95), 'ph': (6.5, 7.0), 'rain': (40, 250)},
        'Coconut': {'n': (15, 40), 'p': (10, 30), 'k': (25, 35), 'temp': (25, 28), 'hum': (90, 99), 'ph': (5.5, 6.5), 'rain': (130, 220)},
        'Cotton': {'n': (100, 140), 'p': (35, 60), 'k': (15, 25), 'temp': (22, 26), 'hum': (75, 85), 'ph': (6.0, 8.0), 'rain': (60, 90)},
        'Jute': {'n': (60, 90), 'p': (35, 60), 'k': (35, 45), 'temp': (23, 26), 'hum': (70, 80), 'ph': (6.0, 7.5), 'rain': (150, 200)},
        'Coffee': {'n': (80, 120), 'p': (15, 35), 'k': (25, 35), 'temp': (23, 28), 'hum': (50, 70), 'ph': (6.0, 7.5), 'rain': (110, 190)}
    }

    data = []
    samples_per_crop = 100
    for crop, cfg in crops_config.items():
        for _ in range(samples_per_crop):
            n = np.clip(np.random.normal(np.mean(cfg['n']), (cfg['n'][1]-cfg['n'][0])/4), 0, 140)
            p = np.clip(np.random.normal(np.mean(cfg['p']), (cfg['p'][1]-cfg['p'][0])/4), 5, 145)
            k = np.clip(np.random.normal(np.mean(cfg['k']), (cfg['k'][1]-cfg['k'][0])/4), 5, 205)
            temp = np.clip(np.random.normal(np.mean(cfg['temp']), (cfg['temp'][1]-cfg['temp'][0])/4), 8, 45)
            hum = np.clip(np.random.normal(np.mean(cfg['hum']), (cfg['hum'][1]-cfg['hum'][0])/4), 14, 100)
            ph = np.clip(np.random.normal(np.mean(cfg['ph']), (cfg['ph'][1]-cfg['ph'][0])/4), 3.5, 10)
            rain = np.clip(np.random.normal(np.mean(cfg['rain']), (cfg['rain'][1]-cfg['rain'][0])/4), 20, 300)
            data.append({
                'N': round(float(n), 2),
                'P': round(float(p), 2),
                'K': round(float(k), 2),
                'temperature': round(float(temp), 2),
                'humidity': round(float(hum), 2),
                'ph': round(float(ph), 2),
                'rainfall': round(float(rain), 2),
                'label': crop
            })

    df = pd.DataFrame(data)
    filepath = os.path.join(DATASET_DIR, 'crop_recommendation.csv')
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} samples in {filepath}")

def generate_yield_prediction_dataset():
    """Generate realistic crop yield dataset (1500 samples)."""
    np.random.seed(42)
    crops = ['Rice', 'Maize', 'Wheat', 'Cotton', 'Sugarcane', 'Potato', 'Tomato', 'Soybean', 'Groundnut', 'Barley']
    soil_types = ['Loamy', 'Clay', 'Sandy', 'Silt', 'Peaty']

    data = []
    for _ in range(1500):
        crop = np.random.choice(crops)
        soil = np.random.choice(soil_types)
        area = np.random.uniform(0.5, 10.0)
        n = np.random.uniform(20, 140)
        p = np.random.uniform(10, 80)
        k = np.random.uniform(15, 150)
        ph = np.random.uniform(5.0, 8.5)
        temp = np.random.uniform(15, 38)
        rainfall = np.random.uniform(300, 1800)
        irrigation_liters = area * np.random.uniform(5000, 25000)
        fertilizer_kg = area * (n*0.5 + p*0.4 + k*0.3)

        base_multiplier = {
            'Rice': 2.8, 'Maize': 3.2, 'Wheat': 2.5, 'Cotton': 1.5,
            'Sugarcane': 35.0, 'Potato': 12.0, 'Tomato': 15.0, 'Soybean': 1.8,
            'Groundnut': 2.0, 'Barley': 2.2
        }[crop]

        # Calculate yield with soil and water quality response
        yield_val = area * base_multiplier * (1 + 0.002*(n+p+k)) * (1 - 0.05*abs(ph-6.5)) * np.random.uniform(0.85, 1.15)
        
        data.append({
            'crop': crop,
            'soil_type': soil,
            'area_acres': round(float(area), 2),
            'nitrogen': round(float(n), 2),
            'phosphorus': round(float(p), 2),
            'potassium': round(float(k), 2),
            'ph': round(float(ph), 2),
            'temperature': round(float(temp), 2),
            'rainfall': round(float(rainfall), 2),
            'irrigation_liters': round(float(irrigation_liters), 2),
            'fertilizer_kg': round(float(fertilizer_kg), 2),
            'yield_tons': round(float(yield_val), 2)
        })

    df = pd.DataFrame(data)
    filepath = os.path.join(DATASET_DIR, 'yield_prediction.csv')
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} samples in {filepath}")

def generate_disease_features_dataset():
    """Generate leaf lesion visual feature dataset for offline classification (1000 samples)."""
    np.random.seed(42)
    diseases = [
        'Healthy',
        'Tomato Early Blight',
        'Potato Late Blight',
        'Rice Brown Spot',
        'Corn Common Rust',
        'Apple Black Rot'
    ]

    data = []
    for _ in range(1200):
        dis = np.random.choice(diseases)
        if dis == 'Healthy':
            h_mean, s_mean, v_mean = np.random.uniform(40, 70), np.random.uniform(100, 200), np.random.uniform(100, 220)
            lesion_ratio = np.random.uniform(0.0, 0.03)
            contrast = np.random.uniform(10, 30)
        elif 'Blight' in dis or 'Rot' in dis:
            h_mean, s_mean, v_mean = np.random.uniform(10, 35), np.random.uniform(80, 180), np.random.uniform(50, 150)
            lesion_ratio = np.random.uniform(0.15, 0.50)
            contrast = np.random.uniform(50, 120)
        else: # Spot or Rust
            h_mean, s_mean, v_mean = np.random.uniform(15, 45), np.random.uniform(120, 220), np.random.uniform(70, 180)
            lesion_ratio = np.random.uniform(0.05, 0.25)
            contrast = np.random.uniform(30, 80)

        data.append({
            'mean_hue': round(float(h_mean), 2),
            'mean_saturation': round(float(s_mean), 2),
            'mean_value': round(float(v_mean), 2),
            'lesion_ratio': round(float(lesion_ratio), 4),
            'texture_contrast': round(float(contrast), 2),
            'disease': dis
        })

    df = pd.DataFrame(data)
    filepath = os.path.join(DATASET_DIR, 'disease_features.csv')
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} samples in {filepath}")

def generate_profit_prediction_dataset():
    """Generate farm profit prediction dataset (1000 samples)."""
    np.random.seed(42)
    crops = ['Rice', 'Maize', 'Wheat', 'Cotton', 'Sugarcane', 'Potato', 'Tomato', 'Soybean']
    
    data = []
    for _ in range(1000):
        crop = np.random.choice(crops)
        area = np.random.uniform(1.0, 15.0)
        yield_tons = area * np.random.uniform(1.5, 18.0)
        price_per_ton = np.random.uniform(200, 1200)
        expected_revenue = yield_tons * price_per_ton
        expenses = area * np.random.uniform(300, 1500)
        profit = expected_revenue - expenses

        data.append({
            'crop': crop,
            'area_acres': round(float(area), 2),
            'yield_tons': round(float(yield_tons), 2),
            'selling_price_per_ton': round(float(price_per_ton), 2),
            'estimated_expenses': round(float(expenses), 2),
            'expected_revenue': round(float(expected_revenue), 2),
            'expected_profit': round(float(profit), 2)
        })

    df = pd.DataFrame(data)
    filepath = os.path.join(DATASET_DIR, 'profit_history.csv')
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} samples in {filepath}")

if __name__ == '__main__':
    generate_crop_recommendation_dataset()
    generate_yield_prediction_dataset()
    generate_disease_features_dataset()
    generate_profit_prediction_dataset()
