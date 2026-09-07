# Smart Farmer Assistant — Security Architecture & Guidelines

## Security Controls Implemented

1. **Password Security**: Werkzeug salted password hashing. Passwords are never stored in plaintext.
2. **Role-Based Access Control (RBAC)**: Custom `@role_required(*roles)` decorator protecting endpoints based on authenticated role (`FARMER`, `ADMIN`, `ADVISOR`).
3. **Login Protection**: Tracks failed login attempts per account. Automatically locks account after 5 consecutive failures.
4. **SQL Injection Prevention**: All database queries are executed via SQLAlchemy ORM parameterized statements.
5. **XSS Protection**: Jinja2 auto-escaping on all rendered template variables.
6. **File Upload Security**: Uploaded leaf images are sanitized with `secure_filename()`, restricted to allowed extensions (`png`, `jpg`, `jpeg`, `webp`, `bmp`), and capped at 16 MB max content length.
7. **Audit Logging**: Comprehensive `AuditLog` table capturing all logins, farmer registrations, admin actions, ML inferences, and report downloads with client IP address logging.
