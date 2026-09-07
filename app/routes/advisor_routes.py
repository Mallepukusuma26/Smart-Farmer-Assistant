from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.middleware.auth_middleware import role_required
from app.models.farmer import Farmer
from app.models.disease import DiseaseDetection
from app.models.soil import SoilRecord
from app.services import NotificationService, AuditService

advisor_bp = Blueprint('advisor', __name__, url_prefix='/advisor')

@advisor_bp.route('/dashboard')
@login_required
@role_required('ADVISOR')
def dashboard():
    advisor = current_user.advisor_profile
    assigned_farmers = Farmer.query.all()  # Advisory view for all active farmers
    recent_diseases = DiseaseDetection.query.order_by(DiseaseDetection.created_at.desc()).limit(8).all()

    return render_template('advisor/dashboard.html',
                           advisor=advisor,
                           farmers=assigned_farmers,
                           recent_diseases=recent_diseases)


@advisor_bp.route('/farmer/<int:farmer_id>', methods=['GET', 'POST'])
@login_required
@role_required('ADVISOR')
def farmer_view(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    farms = farmer.farms.all()
    diseases = DiseaseDetection.query.filter_by(farmer_id=farmer.id).all()

    if request.method == 'POST':
        note = request.form.get('advisory_note')
        NotificationService.create_notification(
            user_id=farmer.user_id,
            title="New Agricultural Advisor Recommendation",
            message=note,
            category='info'
        )
        AuditService.log('ADVISOR_NOTE_SEND', user_id=current_user.id, target_type='Farmer', target_id=farmer.id)
        flash('Advisory recommendation sent to farmer successfully!', 'success')
        return redirect(url_for('advisor.farmer_view', farmer_id=farmer.id))

    return render_template('advisor/farmer_view.html', farmer=farmer, farms=farms, diseases=diseases)
