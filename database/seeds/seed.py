import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    User, Role, Farmer, Advisor, Farm, Field, SoilRecord, Crop, CropCycle,
    Fertilizer, Disease, DiseaseDetection, Expense, Revenue, Notification, AuditLog
)

def seed_database():
    """Populate database with rich agricultural sample data."""
    app = create_app('development')
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding catalog reference crops...")
        crops = [
            Crop(name='Rice', category='Cereal', season='Kharif', min_ph=5.0, max_ph=6.5, min_temp=20, max_temp=30, min_rainfall=180, max_rainfall=300, min_n=90, min_p=40, min_k=40, duration_days=120, base_yield_per_acre=2.8, water_req_mm=1200, description='High water cereal crop.'),
            Crop(name='Maize', category='Cereal', season='Kharif', min_ph=5.5, max_ph=7.0, min_temp=18, max_temp=27, min_rainfall=60, max_rainfall=110, min_n=80, min_p=40, min_k=20, duration_days=95, base_yield_per_acre=3.2, water_req_mm=550, description='Versatile cereal crop.'),
            Crop(name='Wheat', category='Cereal', season='Rabi', min_ph=6.0, max_ph=7.5, min_temp=15, max_temp=25, min_rainfall=45, max_rainfall=100, min_n=100, min_p=50, min_k=40, duration_days=130, base_yield_per_acre=2.5, water_req_mm=450, description='Staple winter cereal crop.'),
            Crop(name='Chickpea', category='Pulse', season='Rabi', min_ph=6.0, max_ph=8.0, min_temp=15, max_temp=25, min_rainfall=40, max_rainfall=90, min_n=25, min_p=60, min_k=80, duration_days=105, base_yield_per_acre=1.2, water_req_mm=300, description='Leguminous protein-rich pulse crop.'),
            Crop(name='Cotton', category='Cash Crop', season='Kharif', min_ph=6.0, max_ph=8.0, min_temp=22, max_temp=32, min_rainfall=60, max_rainfall=120, min_n=120, min_p=50, min_k=20, duration_days=160, base_yield_per_acre=1.5, water_req_mm=750, description='Fiber cash crop.'),
            Crop(name='Potato', category='Vegetable', season='Rabi', min_ph=5.2, max_ph=6.5, min_temp=15, max_temp=22, min_rainfall=50, max_rainfall=80, min_n=140, min_p=60, min_k=100, duration_days=90, base_yield_per_acre=12.0, water_req_mm=500, description='High yield tuber crop.'),
            Crop(name='Tomato', category='Vegetable', season='All Season', min_ph=6.0, max_ph=7.0, min_temp=20, max_temp=30, min_rainfall=40, max_rainfall=90, min_n=110, min_p=50, min_k=80, duration_days=110, base_yield_per_acre=15.0, water_req_mm=600, description='High demand commercial vegetable.'),
            Crop(name='Sugarcane', category='Cash Crop', season='Perennial', min_ph=6.0, max_ph=7.5, min_temp=20, max_temp=38, min_rainfall=150, max_rainfall=250, min_n=150, min_p=60, min_k=90, duration_days=360, base_yield_per_acre=35.0, water_req_mm=1800, description='Long duration sugar cash crop.')
        ]
        db.session.add_all(crops)

        print("Seeding fertilizer catalog...")
        fertilizers = [
            Fertilizer(name='Urea (46% N)', category='Nitrogenous', n_percent=46.0, p_percent=0.0, k_percent=0.0, price_per_kg=22.0, application_notes='Primary nitrogen source.'),
            Fertilizer(name='DAP (18% N, 46% P2O5)', category='Phosphatic', n_percent=18.0, p_percent=46.0, k_percent=0.0, price_per_kg=35.0, application_notes='Ideal basal phosphatic fertilizer.'),
            Fertilizer(name='Muriate of Potash (MOP 60% K2O)', category='Potassic', n_percent=0.0, p_percent=0.0, k_percent=60.0, price_per_kg=30.0, application_notes='Potassium supplement for fruit fill.'),
            Fertilizer(name='NPK 19-19-19', category='Complex', n_percent=19.0, p_percent=19.0, k_percent=19.0, price_per_kg=45.0, application_notes='Balanced water soluble fertilizer.'),
            Fertilizer(name='Neem Cake Organic', category='Organic', n_percent=5.0, p_percent=1.0, k_percent=2.0, price_per_kg=18.0, application_notes='Organic soil conditioner & pest deterrent.')
        ]
        db.session.add_all(fertilizers)

        print("Seeding disease catalog...")
        diseases = [
            Disease(name='Healthy', crop_name='All Crops', symptoms='Vibrant green leaf blade.', cause='None', prevention='Maintain proper field aeration.', organic_treatment='Neem oil spray', chemical_treatment='None'),
            Disease(name='Tomato Early Blight', crop_name='Tomato', symptoms='Concentric brown rings on lower leaves.', cause='Fungal (Alternaria solani)', prevention='Crop rotation & drip irrigation.', organic_treatment='Copper oxychloride spray', chemical_treatment='Mancozeb 75% WP'),
            Disease(name='Potato Late Blight', crop_name='Potato', symptoms='Water-soaked dark lesions.', cause='Fungal (Phytophthora infestans)', prevention='Certified disease-free seed tubers.', organic_treatment='Bordeaux mixture', chemical_treatment='Metalaxyl + Mancozeb'),
            Disease(name='Rice Brown Spot', crop_name='Rice', symptoms='Oval reddish-brown leaf spots.', cause='Fungal (Helminthosporium oryzae)', prevention='Balanced potassic fertilization.', organic_treatment='Pseudomonas fluorescens', chemical_treatment='Carbendazim 50% WP'),
            Disease(name='Corn Common Rust', crop_name='Maize', symptoms='Elongated golden-brown pustules.', cause='Fungal (Puccinia sorghi)', prevention='Resistant hybrid cultivars.', organic_treatment='Sulfur dust', chemical_treatment='Azoxystrobin')
        ]
        db.session.add_all(diseases)
        db.session.commit()

        print("Seeding user accounts (Admin, Advisor, Farmers)...")
        role_farmer = Role(name='FARMER', description='Agricultural Farmer Role')
        role_admin = Role(name='ADMIN', description='System Administrator Role')
        role_advisor = Role(name='ADVISOR', description='Agricultural Advisor Role')
        db.session.add_all([role_farmer, role_admin, role_advisor])
        db.session.flush()

        # 1. Admin User
        admin_user = User(username='admin', email='admin@smartfarmer.org', role='ADMIN', role_id=role_admin.id)
        admin_user.set_password('admin123')
        db.session.add(admin_user)

        # 2. Agricultural Advisor
        advisor_user = User(username='advisor_smith', email='advisor@smartfarmer.org', role='ADVISOR', role_id=role_advisor.id)
        advisor_user.set_password('advisor123')
        db.session.add(advisor_user)
        db.session.flush()

        advisor_profile = Advisor(
            user_id=advisor_user.id,
            full_name='Dr. Robert Smith',
            qualification='Ph.D. Agronomy',
            specialization='Soil & Crop Nutrition',
            region='Midwest Agricultural Zone',
            phone='+1-555-0199'
        )
        db.session.add(advisor_profile)
        db.session.flush()

        # 3. Farmer User 1
        farmer_user = User(username='john_farmer', email='john@smartfarmer.org', role='FARMER', role_id=role_farmer.id)
        farmer_user.set_password('farmer123')
        db.session.add(farmer_user)
        db.session.flush()

        farmer_profile = Farmer(
            user_id=farmer_user.id,
            full_name='John Harvest',
            phone='+1-555-0144',
            address='Green Valley Road, Farm #42',
            region='Central Valley',
            total_land_area=12.5,
            main_crop_type='Maize & Rice',
            experience_years=15,
            assigned_advisor_id=advisor_profile.id
        )
        db.session.add(farmer_profile)
        db.session.flush()

        print("Seeding farms and fields for John Harvest...")
        farm1 = Farm(
            farmer_id=farmer_profile.id,
            name='Sun Valley Homestead',
            location='North Sector, Block A',
            total_area=12.5,
            unit='Acres',
            ownership_type='Owned',
            default_soil_type='Loamy'
        )
        db.session.add(farm1)
        db.session.flush()

        field1 = Field(farm_id=farm1.id, field_name='North Field A1', area=5.0, soil_type='Loamy', irrigation_type='Drip', farming_method='Organic')
        field2 = Field(farm_id=farm1.id, field_name='South Field B2', area=7.5, soil_type='Clay', irrigation_type='Sprinkler', farming_method='Conventional')
        db.session.add_all([field1, field2])
        db.session.flush()

        # Soil Records
        soil1 = SoilRecord(
            field_id=field1.id,
            ph=6.8,
            nitrogen=135.0,
            phosphorus=48.0,
            potassium=190.0,
            moisture=28.0,
            organic_carbon=0.85,
            electrical_conductivity=0.45,
            soil_type='Loamy',
            health_score=88.5,
            deficiency_summary='Optimal condition.',
            recommendation_notes='Maintain current organic compost application schedule.'
        )
        db.session.add(soil1)

        # Expenses & Revenue
        exp1 = Expense(farmer_id=farmer_profile.id, farm_id=farm1.id, field_id=field1.id, category='Seeds', amount=450.0, description='High yield Maize Hybrid Seeds')
        exp2 = Expense(farmer_id=farmer_profile.id, farm_id=farm1.id, field_id=field1.id, category='Fertilizers', amount=320.0, description='Neem Cake & NPK 19-19-19')
        exp3 = Expense(farmer_id=farmer_profile.id, farm_id=farm1.id, field_id=field2.id, category='Irrigation', amount=180.0, description='Drip irrigation maintenance')
        rev1 = Revenue(farmer_id=farmer_profile.id, farm_id=farm1.id, field_id=field1.id, crop_id=crops[1].id, quantity_sold=15.5, unit='Tons', selling_price_per_unit=320.0, total_revenue=4960.0, buyer_name='AgriGrain Logistics')

        db.session.add_all([exp1, exp2, exp3, rev1])

        # Notification & Audit
        notif = Notification(user_id=farmer_user.id, title='Welcome to Smart Farmer Assistant!', message='Your farm account is fully configured. Start by running a soil health check.', category='success')
        audit = AuditLog(user_id=admin_user.id, action='SYSTEM_SEED', details='Populated initial agricultural database records.')
        db.session.add_all([notif, audit])

        db.session.commit()
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    seed_database()
