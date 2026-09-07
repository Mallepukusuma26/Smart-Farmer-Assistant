from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('farmer.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'FARMER').upper()
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        region = request.form.get('region', '').strip()

        if not username or not email or not password:
            flash('Please fill in all required fields.', 'warning')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        user, message = AuthService.register_user(
            username=username,
            email=email,
            password=password,
            role=role,
            full_name=full_name,
            phone=phone,
            address=address,
            region=region
        )

        if not user:
            flash(message, 'danger')
            return render_template('auth/register.html')

        AuditService.log('USER_REGISTER', user_id=user.id, details=f"Registered role {role}")
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_advisor():
            return redirect(url_for('advisor.dashboard'))
        return redirect(url_for('farmer.dashboard'))

    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')

        user, message = AuthService.authenticate_user(username_or_email, password)
        if not user:
            AuditService.log('USER_LOGIN_FAILED', details=f"Target: {username_or_email}")
            flash(message, 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=True)
        AuditService.log('USER_LOGIN', user_id=user.id, details="Login successful")
        flash(f'Welcome back, {user.username}!', 'success')

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif user.is_advisor():
            return redirect(url_for('advisor.dashboard'))
        return redirect(url_for('farmer.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    AuditService.log('USER_LOGOUT', user_id=current_user.id)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        region = request.form.get('region', '').strip()

        success, msg = AuthService.update_profile(current_user.id, full_name, phone, address, region)
        if success:
            flash(msg, 'success')
        else:
            flash(msg, 'danger')

    return render_template('auth/profile.html')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_pass = request.form.get('current_password', '')
        new_pass = request.form.get('new_password', '')
        confirm_pass = request.form.get('confirm_password', '')

        if new_pass != confirm_pass:
            flash('New passwords do not match.', 'danger')
            return render_template('auth/change_password.html')

        success, msg = AuthService.change_password(current_user.id, current_pass, new_pass)
        if success:
            flash(msg, 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(msg, 'danger')

    return render_template('auth/change_password.html')
