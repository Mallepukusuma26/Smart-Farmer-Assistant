import os
from app import create_app
from app.extensions import db
from database.seeds.seed import seed_database

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        
    print(f"Starting Smart Farmer Assistant server on http://127.0.0.1:5050 (Environment: {env})")
    app.run(host='127.0.0.1', port=5050, debug=True)
