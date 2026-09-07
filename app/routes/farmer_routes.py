from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.middleware.auth_middleware import role_required
from app.models.farmer import Farmer
from app.models.farm import Farm
from app.models.field import Field
from app.models.soil import SoilRecord
from app.models.crop import Crop
from app.models.fertilizer import Fertilizer, FertilizerRecommendation
from app.models.irrigation import IrrigationSchedule, IrrigationLog
from app.models.disease import DiseaseDetection
from app.models.yield_prediction import YieldPrediction
from app.models.finance import Expense, Revenue
from app.models.profit_prediction import ProfitPrediction
from app.services import (
    FarmService, SoilService, CropService, FertilizerService,
    IrrigationService, DiseaseService, YieldService, FinanceService,
    ProfitService, ReportService, AuditService
)

farmer_bp = Blueprint('farmer', __name__, url_prefix='/farmer')

def get_farmer_fields(farmer):
    """Ensure farmer has at least one default farm and field plot for forms."""
    farms = farmer.farms.all()
    if not farms:
        farm = FarmService.create_farm(farmer.id, "Main Homestead", "Primary Agricultural Sector", farmer.total_land_area or 10.0, "Acres", "Owned", "Loamy")
        field = FarmService.create_field(farm.id, "North Plot A", farm.total_area, "Loamy", "Drip", "Conventional")
        farms = [farm]
        fields = [field]
    else:
        farm_ids = [f.id for f in farms]
        fields = Field.query.filter(Field.farm_id.in_(farm_ids)).all()
        if not fields:
            field = FarmService.create_field(farms[0].id, "North Plot A", farms[0].total_area, "Loamy", "Drip", "Conventional")
            fields = [field]
    return farms, fields


@farmer_bp.route('/dashboard')
@login_required
@role_required('FARMER')
def dashboard():
    farmer = current_user.farmer_profile
    if not farmer:
        flash('Farmer profile not initialized.', 'warning')
        return redirect(url_for('auth.login'))

    farms, fields = get_farmer_fields(farmer)
    field_ids = [f.id for f in fields]

    soil_records = SoilRecord.query.filter(SoilRecord.field_id.in_(field_ids)).order_by(SoilRecord.test_date.desc()).limit(5).all() if field_ids else []
    diseases = DiseaseDetection.query.filter_by(farmer_id=farmer.id).order_by(DiseaseDetection.created_at.desc()).limit(5).all()
    irrigations = IrrigationSchedule.query.filter(IrrigationSchedule.field_id.in_(field_ids)).order_by(IrrigationSchedule.next_irrigation_date.asc()).limit(5).all() if field_ids else []

    fin_summary = FinanceService.get_financial_summary(farmer.id)

    return render_template('farmer/dashboard.html',
                           farmer=farmer,
                           farms=farms,
                           fields=fields,
                           soil_records=soil_records,
                           diseases=diseases,
                           irrigations=irrigations,
                           fin_summary=fin_summary)


@farmer_bp.route('/farms', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def farms():
    farmer = current_user.farmer_profile
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        total_area = request.form.get('total_area', 1.0)
        unit = request.form.get('unit', 'Acres')
        ownership_type = request.form.get('ownership_type', 'Owned')
        default_soil_type = request.form.get('default_soil_type', 'Loamy')
        notes = request.form.get('notes')

        FarmService.create_farm(farmer.id, name, location, total_area, unit, ownership_type, default_soil_type, notes)
        AuditService.log('FARM_CREATE', user_id=current_user.id, details=f"Created farm {name}")
        flash('Farm created successfully!', 'success')
        return redirect(url_for('farmer.farms'))

    farms_list, _ = get_farmer_fields(farmer)
    return render_template('farmer/farms.html', farms=farms_list)


@farmer_bp.route('/farm/<int:farm_id>', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def farm_detail(farm_id):
    farmer = current_user.farmer_profile
    farm = Farm.query.filter_by(id=farm_id, farmer_id=farmer.id).first_or_404()

    if request.method == 'POST':
        field_name = request.form.get('field_name')
        area = request.form.get('area', 1.0)
        soil_type = request.form.get('soil_type', 'Loamy')
        irrigation_type = request.form.get('irrigation_type', 'Drip')
        farming_method = request.form.get('farming_method', 'Conventional')
        notes = request.form.get('notes')

        FarmService.create_field(farm.id, field_name, area, soil_type, irrigation_type, farming_method, notes)
        AuditService.log('FIELD_CREATE', user_id=current_user.id, details=f"Created field {field_name} in farm {farm.name}")
        flash('Field added successfully!', 'success')
        return redirect(url_for('farmer.farm_detail', farm_id=farm.id))

    fields = farm.fields.all()
    return render_template('farmer/farm_detail.html', farm=farm, fields=fields)


@farmer_bp.route('/soil-analysis', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def soil_analysis():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)

    record = None
    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        ph = request.form.get('ph', type=float)
        nitrogen = request.form.get('nitrogen', type=float)
        phosphorus = request.form.get('phosphorus', type=float)
        potassium = request.form.get('potassium', type=float)
        moisture = request.form.get('moisture', 25.0, type=float)
        organic_carbon = request.form.get('organic_carbon', 0.75, type=float)
        electrical_conductivity = request.form.get('electrical_conductivity', 0.5, type=float)
        soil_type = request.form.get('soil_type', 'Loamy')

        if field_id:
            record = SoilService.analyze_and_save_soil(
                field_id=field_id,
                ph=ph,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                moisture=moisture,
                organic_carbon=organic_carbon,
                electrical_conductivity=electrical_conductivity,
                soil_type=soil_type
            )
            AuditService.log('SOIL_ANALYSIS', user_id=current_user.id, target_type='Field', target_id=field_id, details=f"Score: {record.health_score}")
            flash('Soil analysis completed successfully!', 'success')

    soil_history = SoilRecord.query.filter(SoilRecord.field_id.in_([f.id for f in fields])).order_by(SoilRecord.test_date.desc()).all() if fields else []
    return render_template('farmer/soil_analysis.html', fields=fields, record=record, history=soil_history)


@farmer_bp.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def crop_recommendation():
    recommendations = None
    if request.method == 'POST':
        n = request.form.get('nitrogen', type=float)
        p = request.form.get('phosphorus', type=float)
        k = request.form.get('potassium', type=float)
        temp = request.form.get('temperature', type=float)
        hum = request.form.get('humidity', type=float)
        ph = request.form.get('ph', type=float)
        rain = request.form.get('rainfall', type=float)

        recommendations = CropService.recommend_crops(n, p, k, temp, hum, ph, rain)
        AuditService.log('CROP_RECOMMEND', user_id=current_user.id, details=f"Recommended top: {recommendations[0]['crop_name']}")
        flash('ML Crop recommendation computed!', 'success')

    return render_template('farmer/crop_recommendation.html', recommendations=recommendations)


@farmer_bp.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def fertilizer_recommendation():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)
    crops = Crop.query.order_by(Crop.name.asc()).all()

    rec = None
    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        crop_id = request.form.get('crop_id', type=int) or (crops[0].id if crops else None)
        stage = request.form.get('stage', 'Basal')
        area = request.form.get('area', 1.0, type=float)

        if field_id and crop_id:
            latest_soil = SoilRecord.query.filter_by(field_id=field_id).order_by(SoilRecord.test_date.desc()).first()
            soil_id = latest_soil.id if latest_soil else None

            rec = FertilizerService.calculate_recommendation(field_id, crop_id, soil_id, area_acres=area, growth_stage=stage)
            AuditService.log('FERTILIZER_RECOMMEND', user_id=current_user.id, details=f"Recommended: {rec.recommended_fertilizer}")
            flash('Fertilizer dosage calculated successfully!', 'success')

    rec_history = FertilizerRecommendation.query.filter(FertilizerRecommendation.field_id.in_([f.id for f in fields])).order_by(FertilizerRecommendation.created_at.desc()).all() if fields else []
    return render_template('farmer/fertilizer_recommendation.html', fields=fields, crops=crops, rec=rec, history=rec_history)


@farmer_bp.route('/irrigation', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def irrigation():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)
    crops = Crop.query.order_by(Crop.name.asc()).all()

    schedule = None
    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        crop_id = request.form.get('crop_id', type=int) or (crops[0].id if crops else None)
        moisture = request.form.get('moisture', 25.0, type=float)
        temp = request.form.get('temperature', 28.0, type=float)
        humidity = request.form.get('humidity', 65.0, type=float)
        rainfall = request.form.get('rainfall', 0.0, type=float)

        if field_id:
            schedule = IrrigationService.generate_schedule(field_id, crop_id, soil_moisture=moisture, temperature=temp, humidity=humidity, rainfall_mm=rainfall)
            AuditService.log('IRRIGATION_SCHEDULE', user_id=current_user.id, target_type='Field', target_id=field_id)
            flash('Irrigation schedule updated!', 'success')

    schedules = IrrigationSchedule.query.filter(IrrigationSchedule.field_id.in_([f.id for f in fields])).order_by(IrrigationSchedule.next_irrigation_date.asc()).all() if fields else []
    logs = IrrigationLog.query.filter(IrrigationLog.field_id.in_([f.id for f in fields])).order_by(IrrigationLog.irrigation_date.desc()).all() if fields else []

    return render_template('farmer/irrigation_schedule.html', fields=fields, crops=crops, schedule=schedule, schedules=schedules, logs=logs)


@farmer_bp.route('/disease-detection', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def disease_detection():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)
    detection = None

    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        image_file = request.files.get('leaf_image')

        if image_file and image_file.filename:
            detection = DiseaseService.process_and_diagnose(
                farmer_id=farmer.id,
                image_file=image_file,
                field_id=field_id,
                upload_folder=current_app.config['UPLOAD_FOLDER']
            )
            AuditService.log('DISEASE_DETECT', user_id=current_user.id, details=f"Diagnosed {detection.detected_disease}")
            flash('Leaf image diagnosed successfully!', 'success')
        else:
            flash('Please select a valid image file.', 'warning')

    history = DiseaseDetection.query.filter_by(farmer_id=farmer.id).order_by(DiseaseDetection.created_at.desc()).all()
    return render_template('farmer/disease_detection.html', fields=fields, detection=detection, history=history)


@farmer_bp.route('/yield-prediction', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def yield_prediction():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)
    crops = Crop.query.order_by(Crop.name.asc()).all()

    prediction = None
    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        crop_id = request.form.get('crop_id', type=int) or (crops[0].id if crops else None)
        n = request.form.get('nitrogen', 100.0, type=float)
        p = request.form.get('phosphorus', 40.0, type=float)
        k = request.form.get('potassium', 120.0, type=float)
        ph = request.form.get('ph', 6.5, type=float)
        temp = request.form.get('temperature', 28.0, type=float)
        rain = request.form.get('rainfall', 800.0, type=float)

        if field_id and crop_id:
            prediction = YieldService.predict_yield(field_id, crop_id, n, p, k, ph, temp, rain)
            AuditService.log('YIELD_PREDICT', user_id=current_user.id, details=f"Predicted yield: {prediction.predicted_yield_tons} tons")
            flash('Crop yield predicted successfully!', 'success')

    history = YieldPrediction.query.filter(YieldPrediction.field_id.in_([f.id for f in fields])).order_by(YieldPrediction.created_at.desc()).all() if fields else []
    return render_template('farmer/yield_prediction.html', fields=fields, crops=crops, prediction=prediction, history=history)


@farmer_bp.route('/expenses', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def expenses():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)

    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount', type=float)
        description = request.form.get('description')
        farm_id = request.form.get('farm_id', type=int) or (farms[0].id if farms else None)
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)

        FinanceService.add_expense(farmer.id, category, amount, description, farm_id, field_id)
        AuditService.log('EXPENSE_ADD', user_id=current_user.id, details=f"Expense {category}: ${amount}")
        flash('Expense recorded successfully!', 'success')
        return redirect(url_for('farmer.expenses'))

    expenses_list = Expense.query.filter_by(farmer_id=farmer.id).order_by(Expense.expense_date.desc()).all()
    fin_summary = FinanceService.get_financial_summary(farmer.id)

    return render_template('farmer/expenses.html', expenses=expenses_list, summary=fin_summary, farms=farms, fields=fields)


@farmer_bp.route('/revenue', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def revenue():
    farmer = current_user.farmer_profile
    crops = Crop.query.order_by(Crop.name.asc()).all()

    if request.method == 'POST':
        crop_id = request.form.get('crop_id', type=int) or (crops[0].id if crops else None)
        quantity = request.form.get('quantity_sold', type=float)
        price = request.form.get('selling_price', type=float)
        buyer = request.form.get('buyer_name')
        unit = request.form.get('unit', 'Tons')

        if crop_id:
            FinanceService.add_revenue(farmer.id, crop_id, quantity, price, buyer, unit=unit)
            AuditService.log('REVENUE_ADD', user_id=current_user.id, details=f"Revenue recorded")
            flash('Harvest revenue recorded!', 'success')
            return redirect(url_for('farmer.revenue'))

    revenues_list = Revenue.query.filter_by(farmer_id=farmer.id).order_by(Revenue.sale_date.desc()).all()
    fin_summary = FinanceService.get_financial_summary(farmer.id)

    return render_template('farmer/revenue.html', revenues=revenues_list, summary=fin_summary, crops=crops)


@farmer_bp.route('/profit-prediction', methods=['GET', 'POST'])
@login_required
@role_required('FARMER')
def profit_prediction():
    farmer = current_user.farmer_profile
    farms, fields = get_farmer_fields(farmer)
    crops = Crop.query.order_by(Crop.name.asc()).all()

    prediction = None
    if request.method == 'POST':
        field_id = request.form.get('field_id', type=int) or (fields[0].id if fields else None)
        crop_id = request.form.get('crop_id', type=int) or (crops[0].id if crops else None)
        yield_tons = request.form.get('expected_yield_tons', type=float)
        price = request.form.get('expected_selling_price', type=float)
        expenses = request.form.get('estimated_expenses', type=float)

        if field_id and crop_id:
            prediction = ProfitService.predict_profit(farmer.id, field_id, crop_id, yield_tons, price, expenses)
            AuditService.log('PROFIT_PREDICT', user_id=current_user.id, details=f"Expected profit: ${prediction.expected_profit}")
            flash('Farm profit forecast calculated!', 'success')

    history = ProfitPrediction.query.filter_by(farmer_id=farmer.id).order_by(ProfitPrediction.created_at.desc()).all()
    return render_template('farmer/profit_prediction.html', fields=fields, crops=crops, prediction=prediction, history=history)
