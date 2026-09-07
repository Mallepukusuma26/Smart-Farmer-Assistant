import os
from flask import Blueprint, send_from_directory, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.report import Report
from app.models.finance import Expense
from app.services import ReportService, FinanceService, AuditService

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/download/<path:filename>')
@login_required
def download_report(filename):
    reports_dir = current_app.config['REPORT_FOLDER']
    AuditService.log('REPORT_DOWNLOAD', user_id=current_user.id, details=f"Downloaded {filename}")
    return send_from_directory(reports_dir, filename, as_attachment=True)


@report_bp.route('/generate-pdf/<report_type>')
@login_required
def generate_pdf(report_type):
    farmer = current_user.farmer_profile
    if not farmer:
        flash('Only registered farmers can generate reports.', 'warning')
        return redirect(url_for('farmer.dashboard'))

    fin_summary = FinanceService.get_financial_summary(farmer.id)
    data = {
        'farmer_name': farmer.full_name,
        'region': farmer.region,
        'total_land_area': f"{farmer.total_land_area} Acres",
        'total_expenses': f"${fin_summary['total_expense']}",
        'total_revenue': f"${fin_summary['total_revenue']}",
        'net_profit': f"${fin_summary['net_profit']}",
        'profit_margin': f"{fin_summary['profit_margin_percent']}%"
    }

    rep = ReportService.generate_farmer_pdf_report(farmer.id, report_type.title(), data, current_app.config['REPORT_FOLDER'])
    AuditService.log('REPORT_GENERATE_PDF', user_id=current_user.id, details=f"Generated {report_type}")
    flash('PDF report generated successfully!', 'success')
    return redirect(url_for('report.download_report', filename=os.path.basename(rep.file_path)))


@report_bp.route('/export-expenses-csv')
@login_required
def export_expenses_csv():
    farmer = current_user.farmer_profile
    if not farmer:
        flash('Access restricted.', 'warning')
        return redirect(url_for('farmer.dashboard'))

    expenses_list = Expense.query.filter_by(farmer_id=farmer.id).all()
    rep = ReportService.export_expenses_csv(farmer.id, expenses_list, current_app.config['REPORT_FOLDER'])
    AuditService.log('REPORT_EXPORT_CSV', user_id=current_user.id)
    flash('CSV Export generated successfully!', 'success')
    return redirect(url_for('report.download_report', filename=os.path.basename(rep.file_path)))
