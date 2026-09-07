# Multi-stage Reproducible Dockerfile for Smart Farmer Assistant
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt

COPY . .

# Final runtime image
FROM python:3.12-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
EXPOSE 5050

CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "5050", "--no-debug"]
