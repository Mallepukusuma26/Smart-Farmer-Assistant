import os
from datetime import datetime
from app.extensions import db
from app.models.report import Report
from app.models.farmer import Farmer
from app.utils.pdf_generator import PDFReportGenerator
from app.utils.csv_generator import CSVReportGenerator

class ReportService:
    """Service layer for report generation and retrieval."""

    @staticmethod
    def generate_farmer_pdf_report(farmer_id, report_type, data_dict, reports_dir='reports'):
        """Generate PDF report and record in database."""
        farmer = Farmer.query.get(farmer_id)
        farmer_name = farmer.full_name if farmer else 'Farmer'

        filename = f"{report_type.lower().replace(' ', '_')}_{farmer_id}_{int(datetime.utcnow().timestamp())}.pdf"
        file_path = os.path.join(reports_dir, filename)

        PDFReportGenerator.generate_pdf(
            output_path=file_path,
            title=f"{report_type} — {farmer_name}",
            report_type=report_type,
            data_dict=data_dict
        )

        rep = Report(
            farmer_id=farmer_id,
            report_type=report_type,
            title=f"{report_type} ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='pdf'
        )

        db.session.add(rep)
        db.session.commit()
        return rep

    @staticmethod
    def export_expenses_csv(farmer_id, expenses_list, reports_dir='reports'):
        """Export farmer expenses list as CSV file."""
        filename = f"expenses_export_{farmer_id}_{int(datetime.utcnow().timestamp())}.csv"
        file_path = os.path.join(reports_dir, filename)

        headers = ['ID', 'Date', 'Category', 'Amount ($)', 'Description']
        rows = [
            [e.id, e.expense_date.strftime('%Y-%m-%d'), e.category, e.amount, e.description or '']
            for e in expenses_list
        ]

        CSVReportGenerator.generate_csv(file_path, headers, rows)

        rep = Report(
            farmer_id=farmer_id,
            report_type='Expense CSV Export',
            title=f"Expenses CSV Export ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='csv'
        )

        db.session.add(rep)
        db.session.commit()
        return rep
