# Smart Farmer Assistant — Deployment Guide

## Production Deployment Overview

Smart Farmer Assistant can be deployed on Linux / Windows servers using Gunicorn or Waitress WSGI server with Nginx as a reverse proxy.

### WSGI Server Configuration (Waitress / Gunicorn)

To run with Gunicorn:
```bash
gunicorn --workers 4 --bind 127.0.0.1:5000 "app:create_app('production')"
```

To run on Windows with Waitress:
```bash
pip install waitress
waitress-serve --port=5000 "app:create_app('production')"
```

### Environment Variables
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Long random secret key
- `DATABASE_URL`: `sqlite:///instance/smart_farmer_prod.db` (or MySQL URI `mysql+pymysql://user:pass@localhost/db`)
