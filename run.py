"""
Executable Entry Point for Smart Farmer Assistant.

Supports running Flask development web server, database auto-initialization,
seeding reference datasets, and local machine learning model training.
"""

import os
import sys
import argparse
from app import create_app
from app.extensions import db
from database.seeds.seed import seed_database
from scripts.retrain_models import retrain_all_models

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)


def main():
    parser = argparse.ArgumentParser(description="Smart Farmer Assistant Executable Entry Point")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address to bind server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5050, help="Port to run Flask server (default: 5050)")
    parser.add_argument("--seed", action="store_true", help="Seed database with sample agricultural datasets")
    parser.add_argument("--retrain-models", action="store_true", help="Retrain offline ML models")
    parser.add_argument("--no-debug", action="store_true", help="Disable Flask debug mode")

    args = parser.parse_args()

    with app.app_context():
        db.create_all()
        if args.seed:
            print("=== Seeding Database ===")
            seed_database()
            print("=== Database Seeded Successfully ===")

    if args.retrain_models:
        print("=== Retraining Machine Learning Models ===")
        retrain_all_models()

    debug_flag = not args.no_debug
    print(f"================================================================")
    print(f" SMART FARMER ASSISTANT — SERVER STARTED")
    print(f" Environment : {env}")
    print(f" URL         : http://{args.host}:{args.port}")
    print(f" Debug Mode  : {debug_flag}")
    print(f"================================================================")

    app.run(host=args.host, port=args.port, debug=debug_flag)


if __name__ == "__main__":
    main()
