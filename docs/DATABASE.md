# Smart Farmer Assistant — Database Schema Documentation

## Entity Relationship Summary

The application uses SQLAlchemy ORM with SQLite by default. Key entities include:

- `users`: Authentication credentials, passwords, role (`FARMER`, `ADMIN`, `ADVISOR`), active status, failed attempts, lock status.
- `farmers`: Farmer profile details linked 1-to-1 with `users`.
- `advisors`: Agricultural advisor profile linked 1-to-1 with `users`.
- `farms`: Farm property belonging to a farmer.
- `fields`: Field plot division belonging to a farm.
- `soil_records`: Soil testing records (pH, N, P, K, Organic Carbon, EC, health score) belonging to a field.
- `crops`: Catalog of reference crops and agro-climatic requirements.
- `crop_cycles`: Active or completed crop cultivation cycles on a field plot.
- `fertilizers`: Fertilizer catalog (N-P-K percentages, pricing per kg).
- `fertilizer_recommendations`: Calculated fertilizer dosage recommendations for a field.
- `irrigation_schedules`: Calculated daily water volume, frequency, and next date schedules.
- `irrigation_logs`: Completed watering logs.
- `diseases`: Knowledge base catalog of crop leaf diseases and treatments.
- `disease_detections`: Diagnostic log of leaf image uploads and model predictions.
- `yield_predictions`: Crop yield regression predictions.
- `expenses`: Farm expenditures categorized by Seeds, Fertilizers, Labour, Irrigation, Fuel, etc.
- `revenues`: Harvest crop sales records.
- `profit_predictions`: Financial profit forecast predictions.
- `notifications`: Internal user notifications.
- `reports`: Generated PDF/CSV report file registry.
- `audit_logs`: System operation and security audit trail.
