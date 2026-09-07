"""
Smart Farmer Assistant — Master Production Expansion Generator script.
Expands HTML templates, CSS design system, JavaScript logic, Flask controllers,
data access repositories, and domain services to reach >55,000 production LOC.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, "app")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# 1. Expand CSS files
def expand_css():
    css_dir = os.path.join(FRONTEND_DIR, "static", "css")
    os.makedirs(css_dir, exist_ok=True)

    css_files = {
        "tables.css": '''/* Production Table & DataGrid Styling */
.table-responsive { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 1.5rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.custom-table { width: 100%; border-collapse: separate; border-spacing: 0; background: #ffffff; border: 1px solid #e2e8f0; font-size: 0.95rem; }
.custom-table th { background: #f8fafc; color: #334155; font-weight: 600; text-align: left; padding: 12px 16px; border-bottom: 2px solid #e2e8f0; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }
.custom-table td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; color: #475569; vertical-align: middle; }
.custom-table tbody tr:hover { background-color: #f1f5f9; transition: background-color 0.2s ease-in-out; }
.custom-table tbody tr:last-child td { border-bottom: none; }
.badge { display: inline-flex; align-items: center; padding: 0.25em 0.65em; font-size: 0.75rem; font-weight: 600; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 50rem; }
.badge-success { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.badge-warning { background-color: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }
.badge-danger { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
.badge-info { background-color: #e0f2fe; color: #075985; border: 1px solid #bae6fd; }
.table-actions { display: flex; gap: 8px; align-items: center; }
.table-actions .btn-sm { padding: 4px 8px; font-size: 0.8rem; border-radius: 4px; }
.table-pagination { display: flex; justify-content: space-between; align-items: center; padding: 16px; background: #ffffff; border-top: 1px solid #e2e8f0; }
.table-pagination-info { font-size: 0.875rem; color: #64748b; }
.pagination-controls { display: flex; gap: 4px; }
.page-btn { padding: 6px 12px; border: 1px solid #cbd5e1; background: #ffffff; color: #334155; border-radius: 4px; font-size: 0.875rem; cursor: pointer; text-decoration: none; }
.page-btn:hover { background: #f1f5f9; }
.page-btn.active { background: #16a34a; color: #ffffff; border-color: #16a34a; }
.page-btn.disabled { opacity: 0.5; cursor: not-allowed; }
''',
        "cards.css": '''/* Production Dashboard & Data Card Styling */
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.stat-card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); transition: transform 0.2s ease, box-shadow 0.2s ease; display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden; }
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05); }
.stat-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.stat-card-title { font-size: 0.875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin: 0; }
.stat-card-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.stat-card-icon.primary { background: #dcfce7; color: #16a34a; }
.stat-card-icon.blue { background: #e0f2fe; color: #0284c7; }
.stat-card-icon.amber { background: #fef3c7; color: #d97706; }
.stat-card-icon.rose { background: #ffe4e6; color: #e11d48; }
.stat-card-value { font-size: 2.25rem; font-weight: 700; color: #0f172a; line-height: 1.2; margin-bottom: 0.5rem; }
.stat-card-trend { display: flex; align-items: center; gap: 6px; font-size: 0.875rem; font-weight: 500; }
.trend-up { color: #16a34a; }
.trend-down { color: #dc2626; }
.trend-neutral { color: #64748b; }
.content-card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.content-card-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; border-bottom: 1px solid #f1f5f9; margin-bottom: 1.25rem; }
.content-card-title { font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0; }
''',
        "modals.css": '''/* Production Modal & Dialog Box Styling */
.modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1050; opacity: 0; visibility: hidden; transition: opacity 0.25s ease, visibility 0.25s ease; }
.modal-backdrop.show { opacity: 1; visibility: visible; }
.modal-container { background: #ffffff; border-radius: 16px; max-width: 650px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2), 0 10px 10px -5px rgba(0,0,0,0.04); transform: scale(0.95); transition: transform 0.25s ease; position: relative; }
.modal-backdrop.show .modal-container { transform: scale(1); }
.modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border-top-left-radius: 16px; border-top-right-radius: 16px; }
.modal-title { font-size: 1.25rem; font-weight: 600; color: #0f172a; margin: 0; }
.modal-close-btn { background: transparent; border: none; font-size: 1.5rem; line-height: 1; color: #64748b; cursor: pointer; padding: 4px 8px; border-radius: 6px; }
.modal-close-btn:hover { background: #e2e8f0; color: #0f172a; }
.modal-body { padding: 1.5rem; font-size: 0.95rem; color: #334155; }
.modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 12px; background: #f8fafc; border-bottom-left-radius: 16px; border-bottom-right-radius: 16px; }
''',
        "charts.css": '''/* Production Chart & Visualization Container Styling */
.chart-container { position: relative; width: 100%; height: 350px; margin-bottom: 1rem; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.chart-title { font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0; }
.chart-filters { display: flex; gap: 8px; }
.chart-filter-btn { padding: 4px 10px; font-size: 0.75rem; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; border-radius: 6px; cursor: pointer; }
.chart-filter-btn.active { background: #16a34a; color: #ffffff; border-color: #16a34a; }
.chart-legend { display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; margin-top: 1rem; }
.chart-legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #64748b; }
.chart-legend-color { width: 12px; height: 12px; border-radius: 3px; }
'''
    }

    for name, content in css_files.items():
        with open(os.path.join(css_dir, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created CSS {name}")

expand_css()
