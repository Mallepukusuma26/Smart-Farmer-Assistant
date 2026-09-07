import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.repositories.report_repository import ReportRepository
from app.models.report import Report
from app.models.farmer import Farmer
from app.utils.pdf_generator import PDFReportGenerator
from app.utils.csv_generator import CSVReportGenerator

class ReportService:
    """Domain Service for PDF, CSV, JSON, and HTML report generation across all 16 agricultural modules."""

    def __init__(self, repository: Optional[ReportRepository] = None):
        self.repository = repository or ReportRepository()

    def generate_pdf_report(
        self,
        farmer_id: int,
        report_type: str,
        data_dict: Dict[str, Any],
        farm_id: Optional[int] = None,
        reports_dir: str = 'reports'
    ) -> Report:
        """Generate formatted PDF report document and persist file reference."""
        os.makedirs(reports_dir, exist_ok=True)
        farmer = Farmer.query.get(farmer_id)
        farmer_name = farmer.full_name if farmer else 'Farmer'

        filename = f"{report_type.lower().replace(' ', '_')}_{farmer_id}_{int(datetime.utcnow().timestamp())}.pdf"
        file_path = os.path.join(reports_dir, filename)

        title_str = f"{report_type} — {farmer_name}"
        PDFReportGenerator.generate_pdf(
            output_path=file_path,
            title=title_str,
            report_type=report_type,
            data_dict=data_dict
        )

        size_kb = round(os.path.getsize(file_path) / 1024.0, 1) if os.path.exists(file_path) else 0.0

        return self.repository.save_report(
            farmer_id=farmer_id,
            farm_id=farm_id,
            report_type=report_type,
            title=f"{report_type} ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='pdf',
            file_size_kb=size_kb,
            parameters=json.dumps({'farmer_id': farmer_id, 'report_type': report_type})
        )

    def export_expenses_csv(self, farmer_id: int, expenses_list: List[Any], reports_dir: str = 'reports') -> Report:
        """Export itemized farm expense history as a downloadable CSV spreadsheet."""
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"expenses_export_{farmer_id}_{int(datetime.utcnow().timestamp())}.csv"
        file_path = os.path.join(reports_dir, filename)

        headers = ['ID', 'Date', 'Category', 'Amount ($)', 'Payment Method', 'Vendor', 'Description']
        rows = [
            [
                e.id,
                e.expense_date.strftime('%Y-%m-%d') if hasattr(e, 'expense_date') and e.expense_date else '',
                getattr(e, 'category', ''),
                getattr(e, 'amount', 0.0),
                getattr(e, 'payment_method', 'Cash'),
                getattr(e, 'vendor_name', ''),
                getattr(e, 'description', '')
            ]
            for e in expenses_list
        ]

        CSVReportGenerator.generate_csv(file_path, headers, rows)
        size_kb = round(os.path.getsize(file_path) / 1024.0, 1) if os.path.exists(file_path) else 0.0

        return self.repository.save_report(
            farmer_id=farmer_id,
            report_type='Expense CSV Export',
            title=f"Expenses CSV Export ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='csv',
            file_size_kb=size_kb
        )

    def export_json_report(self, farmer_id: int, report_type: str, data_dict: Dict[str, Any], reports_dir: str = 'reports') -> Report:
        """Export structured report dataset as downloadable JSON file."""
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"{report_type.lower().replace(' ', '_')}_{farmer_id}_{int(datetime.utcnow().timestamp())}.json"
        file_path = os.path.join(reports_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, default=str)

        size_kb = round(os.path.getsize(file_path) / 1024.0, 1) if os.path.exists(file_path) else 0.0

        return self.repository.save_report(
            farmer_id=farmer_id,
            report_type=report_type,
            title=f"{report_type} JSON Export ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='json',
            file_size_kb=size_kb
        )

    def export_html_report(self, farmer_id: int, report_type: str, html_content: str, reports_dir: str = 'reports') -> Report:
        """Export printable HTML report page."""
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"{report_type.lower().replace(' ', '_')}_{farmer_id}_{int(datetime.utcnow().timestamp())}.html"
        file_path = os.path.join(reports_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        size_kb = round(os.path.getsize(file_path) / 1024.0, 1) if os.path.exists(file_path) else 0.0

        return self.repository.save_report(
            farmer_id=farmer_id,
            report_type=report_type,
            title=f"{report_type} Printable HTML ({datetime.now().strftime('%b %d, %Y')})",
            file_path=filename,
            file_format='html',
            file_size_kb=size_kb
        )
