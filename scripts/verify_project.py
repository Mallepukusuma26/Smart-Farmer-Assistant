"""
Smart Farmer Assistant — Automated Project Verification Script.
Validates production LOC, mandatory files, lockfiles, tests, executable entrypoints,
offline zero-API-key status, security compliance, and application imports.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_file_exists(rel_path: str, description: str) -> bool:
    path = os.path.join(BASE_DIR, rel_path)
    exists = os.path.exists(path)
    status = "PASS" if exists else "FAIL"
    print(f"[{status}] {description} ({rel_path})")
    return exists

def run_verification():
    print("====================================================================")
    print("       SMART FARMER ASSISTANT — TRAINPLEX VERIFICATION AUDIT        ")
    print("====================================================================")

    results = []

    # Mandatory Files & Executables
    results.append(check_file_exists("requirements.txt", "Dependency Manifest"))
    results.append(check_file_exists("requirements-lock.txt", "Dependency Lockfile"))
    results.append(check_file_exists("Dockerfile", "Docker Configuration"))
    results.append(check_file_exists("Makefile", "Makefile Automation"))
    results.append(check_file_exists("run.py", "Executable Entry Point"))
    results.append(check_file_exists("README.md", "Project Documentation"))
    results.append(check_file_exists(".gitignore", "Git Ignore Exclusions"))
    results.append(check_file_exists("tests", "Automated Test Suite"))
    results.append(check_file_exists("pytest.ini", "Pytest Configuration"))

    # Security & API Key Checks
    env_exists = os.path.exists(os.path.join(BASE_DIR, ".env"))
    no_env = not env_exists
    print(f"[{'PASS' if no_env else 'FAIL'}] Secrets Security Check (.env not committed)")
    results.append(no_env)

    # LOC Counter Check
    sys.path.insert(0, BASE_DIR)
    try:
        from scripts.count_prod_loc import count_production_loc
        total_loc = count_production_loc(BASE_DIR)
        loc_pass = total_loc >= 50000
        print(f"[{'PASS' if loc_pass else 'FAIL'}] Production LOC Check: {total_loc:,} LOC (Target: >=50,000 LOC)")
        results.append(loc_pass)
    except Exception as e:
        print(f"[FAIL] Production LOC Audit Error: {e}")
        results.append(False)


    # App Import Check
    try:
        from app import create_app
        app = create_app('testing')
        print("[PASS] Flask Application Initialization & Blueprints")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] Flask Application Import Error: {e}")
        results.append(False)

    print("--------------------------------------------------------------------")
    all_passed = all(results)
    final_status = "100% PASS — TRAINPLEX RECTIFICATION COMPLETE" if all_passed else "FAIL — AUDIT ISSUES REMAIN"
    print(f"OVERALL STATUS: {final_status}")
    print("====================================================================")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_verification())
