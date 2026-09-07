from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.middleware.auth_middleware import role_required
from app.extensions import db
from app.models.user import User
from app.models.farmer import Farmer
from app.models.advisor import Advisor
from app.models.crop import Crop
from app.models.fertilizer import Fertilizer
from app.models.disease import Disease
from app.models.audit import AuditLog
from app.services import AuditService
from ml.visualizations.model_plots import get_crop_model_comparison_metrics, get_yield_model_comparison_metrics

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('ADMIN')
def dashboard():
    total_users = User.query.count()
    total_farmers = User.query.filter_by(role='FARMER').count()
    total_advisors = User.query.filter_by(role='ADVISOR').count()
    total_crops = Crop.query.count()
    total_diseases = Disease.query.count()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()
    crop_metrics = get_crop_model_comparison_metrics()
    yield_metrics = get_yield_model_comparison_metrics()

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_farmers=total_farmers,
                           total_advisors=total_advisors,
                           total_crops=total_crops,
                           total_diseases=total_diseases,
                           recent_logs=recent_logs,
                           crop_metrics=crop_metrics,
                           yield_metrics=yield_metrics)


@admin_bp.route('/users')
@login_required
@role_required('ADMIN')
def users():
    user_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=user_list)


@admin_bp.route('/user/toggle/<int:user_id>')
@login_required
@role_required('ADMIN')
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate yourself.', 'warning')
        return redirect(url_for('admin.users'))

    user.is_active = not user.is_active
    db.session.commit()
    AuditService.log('ADMIN_USER_TOGGLE', user_id=current_user.id, target_type='User', target_id=user.id)
    flash(f"User {user.username} status updated to {'Active' if user.is_active else 'Inactive'}.", 'info')
    return redirect(url_for('admin.users'))


@admin_bp.route('/crops', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def crops():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        season = request.form.get('season')
        min_ph = request.form.get('min_ph', 5.5, type=float)
        max_ph = request.form.get('max_ph', 7.5, type=float)

        crop = Crop(name=name, category=category, season=season, min_ph=min_ph, max_ph=max_ph)
        db.session.add(crop)
        db.session.commit()
        AuditService.log('ADMIN_CROP_ADD', user_id=current_user.id, details=f"Added crop {name}")
        flash(f'Crop {name} added to catalog!', 'success')
        return redirect(url_for('admin.crops'))

    crop_list = Crop.query.all()
    return render_template('admin/crops.html', crops=crop_list)


@admin_bp.route('/fertilizers', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def fertilizers():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        n = request.form.get('n_percent', 0.0, type=float)
        p = request.form.get('p_percent', 0.0, type=float)
        k = request.form.get('k_percent', 0.0, type=float)
        price = request.form.get('price_per_kg', 25.0, type=float)

        fert = Fertilizer(name=name, category=category, n_percent=n, p_percent=p, k_percent=k, price_per_kg=price)
        db.session.add(fert)
        db.session.commit()
        AuditService.log('ADMIN_FERTILIZER_ADD', user_id=current_user.id, details=f"Added fertilizer {name}")
        flash(f'Fertilizer {name} added!', 'success')
        return redirect(url_for('admin.fertilizers'))

    fert_list = Fertilizer.query.all()
    return render_template('admin/fertilizers.html', fertilizers=fert_list)


@admin_bp.route('/diseases', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def diseases():
    if request.method == 'POST':
        name = request.form.get('name')
        crop_name = request.form.get('crop_name')
        symptoms = request.form.get('symptoms')
        prevention = request.form.get('prevention')

        dis = Disease(name=name, crop_name=crop_name, symptoms=symptoms, prevention=prevention)
        db.session.add(dis)
        db.session.commit()
        AuditService.log('ADMIN_DISEASE_ADD', user_id=current_user.id, details=f"Added disease {name}")
        flash(f'Disease {name} recorded in catalog!', 'success')
        return redirect(url_for('admin.diseases'))

    disease_list = Disease.query.all()
    return render_template('admin/diseases.html', diseases=disease_list)


@admin_bp.route('/audit-logs')
@login_required
@role_required('ADMIN')
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template('admin/audit_logs.html', logs=logs)
