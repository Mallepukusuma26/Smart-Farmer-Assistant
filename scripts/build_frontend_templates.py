"""
Build Comprehensive Frontend HTML Templates for Smart Farmer Assistant.
Creates high-density production templates across farmer, admin, and advisor portals.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")
FARMER_DIR = os.path.join(TEMPLATES_DIR, "farmer")
ADMIN_DIR = os.path.join(TEMPLATES_DIR, "admin")
ADVISOR_DIR = os.path.join(TEMPLATES_DIR, "advisor")

os.makedirs(FARMER_DIR, exist_ok=True)
os.makedirs(ADMIN_DIR, exist_ok=True)
os.makedirs(ADVISOR_DIR, exist_ok=True)

# 1. Farmer Crop Rotation Planner Template
crop_rotation_html = '''{% extends "base.html" %}
{% block title %}Crop Rotation Planner — Smart Farmer Assistant{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1 class="h3 mb-0 text-gray-800">Multi-Season Crop Rotation Planner</h1>
            <p class="text-muted mb-0">Optimize soil nutrient balance, reduce disease carryover, and maximize farm yield profitability.</p>
        </div>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newRotationModal">
            <i class="fas fa-sync-alt me-2"></i>Generate Rotation Plan
        </button>
    </div>

    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-3 p-3">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 bg-success bg-opacity-10 text-success rounded-3 p-3">
                        <i class="fas fa-layer-group fa-2x"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <div class="text-muted small">Total Fields Planned</div>
                        <div class="h4 mb-0 fw-bold">12 Fields</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-3 p-3">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 bg-primary bg-opacity-10 text-primary rounded-3 p-3">
                        <i class="fas fa-seedling fa-2x"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <div class="text-muted small">Nitrogen Fixation Legumes</div>
                        <div class="h4 mb-0 fw-bold">35% Area</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-3 p-3">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 bg-warning bg-opacity-10 text-warning rounded-3 p-3">
                        <i class="fas fa-shield-virus fa-2x"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <div class="text-muted small">Disease Break Index</div>
                        <div class="h4 mb-0 fw-bold">92 / 100</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-3 p-3">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 bg-info bg-opacity-10 text-info rounded-3 p-3">
                        <i class="fas fa-chart-line fa-2x"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <div class="text-muted small">Projected Yield Boost</div>
                        <div class="h4 mb-0 fw-bold">+18.5%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0 fw-bold text-gray-800">4-Season Field Crop Sequencing Schedule</h5>
            <div class="btn-group">
                <button class="btn btn-outline-secondary btn-sm">2025-2026</button>
                <button class="btn btn-outline-secondary btn-sm active">2026-2027</button>
            </div>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0 custom-table">
                    <thead class="table-light">
                        <tr>
                            <th>Field Name</th>
                            <th>Soil Type</th>
                            <th>Kharif (Monsoon)</th>
                            <th>Rabi (Winter)</th>
                            <th>Zaid (Summer)</th>
                            <th>Soil N Balance</th>
                            <th>Disease Score</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="fw-bold">North Field A1 (5.2 Acres)</td>
                            <td>Clay Loam</td>
                            <td><span class="badge bg-success">Rice (Paddy)</span></td>
                            <td><span class="badge bg-primary">Chickpea (Legume)</span></td>
                            <td><span class="badge bg-warning text-dark">Green Gram</span></td>
                            <td><span class="text-success fw-bold">+35 kg N/ha</span></td>
                            <td><span class="badge bg-success">Optimal</span></td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary"><i class="fas fa-edit"></i></button>
                                <button class="btn btn-sm btn-outline-info"><i class="fas fa-chart-pie"></i></button>
                            </td>
                        </tr>
                        <tr>
                            <td class="fw-bold">South Field B2 (8.0 Acres)</td>
                            <td>Sandy Loam</td>
                            <td><span class="badge bg-warning text-dark">Maize</span></td>
                            <td><span class="badge bg-info text-dark">Wheat</span></td>
                            <td><span class="badge bg-secondary">Fallow / Cover Crop</span></td>
                            <td><span class="text-danger fw-bold">-15 kg N/ha</span></td>
                            <td><span class="badge bg-warning text-dark">Moderate Risk</span></td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary"><i class="fas fa-edit"></i></button>
                                <button class="btn btn-sm btn-outline-info"><i class="fas fa-chart-pie"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

with open(os.path.join(FARMER_DIR, "crop_rotation.html"), "w", encoding="utf-8") as f:
    f.write(crop_rotation_html)

print("Created crop_rotation.html")
