"""
Comprehensive Report Service Module for Smart Farmer Assistant.

Generates structured HTML, CSV, and JSON printable reports for farmers, farms, fields,
soil test histories, crop recommendations, fertilizer schedules, irrigation water budgets,
disease diagnoses, yield predictions, and financial accounting.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ComprehensiveReportService:
    """
    Export engine for multi-format (HTML, CSV, JSON) reporting across all agricultural sub-systems.
    """

    def generate_farmer_master_report_json(self, farmer_id: int, summary_data: Dict[str, Any]) -> str:
        """
        Exports comprehensive farmer profile and operations state as a formatted JSON document.
        """
        report_payload = {
            "report_type": "Smart Farmer Assistant - Master Agricultural Report",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "farmer_id": farmer_id,
            "data": summary_data
        }
        return json.dumps(report_payload, indent=2)

    def generate_soil_health_csv_report(self, soil_records: List[Dict[str, Any]]) -> str:
        """
        Generates CSV format string for historical soil test records.
        """
        headers = ["Test Date", "Field Name", "pH", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Organic Carbon %", "Health Score %"]
        lines = [",".join(headers)]

        for r in soil_records:
            row = [
                str(r.get("test_date", "")),
                str(r.get("field_name", "Plot 1")),
                str(r.get("ph", 7.0)),
                str(r.get("nitrogen", 0.0)),
                str(r.get("phosphorus", 0.0)),
                str(r.get("potassium", 0.0)),
                str(r.get("organic_carbon", 0.75)),
                str(r.get("health_score", 75.0))
            ]
            lines.append(",".join(row))

        return "\n".join(lines)

    def generate_financial_summary_html_report(self, financial_data: Dict[str, Any]) -> str:
        """
        Generates clean HTML markup string for printing farm financial P&L summary.
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Farm Financial Summary Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
                h2 {{ color: #1b4332; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                th {{ background-color: #2d6a4f; color: white; }}
                .highlight {{ font-weight: bold; color: #1b4332; }}
            </style>
        </head>
        <body>
            <h2>Smart Farmer Assistant — Farm Financial P&L Statement</h2>
            <p><strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <table>
                <tr><th>Metric</th><th>Value (INR)</th></tr>
                <tr><td>Total Registered Land Area</td><td>{financial_data.get('total_land_acres', 1.0)} Acres</td></tr>
                <tr><td>Total Farm Expenses</td><td>₹ {financial_data.get('total_expenses', 0.0):,}</td></tr>
                <tr><td>Total Gross Revenue</td><td>₹ {financial_data.get('total_revenue', 0.0):,}</td></tr>
                <tr class="highlight"><td>Net Operating Profit</td><td>₹ {financial_data.get('net_profit', 0.0):,}</td></tr>
                <tr><td>Cost Per Acre</td><td>₹ {financial_data.get('cost_per_acre', 0.0):,}</td></tr>
                <tr><td>Profit Per Acre</td><td>₹ {financial_data.get('profit_per_acre', 0.0):,}</td></tr>
                <tr><td>Return on Investment (ROI)</td><td>{financial_data.get('roi_percentage', 0.0)} %</td></tr>
            </table>
        </body>
        </html>
        """
        return html.strip()
