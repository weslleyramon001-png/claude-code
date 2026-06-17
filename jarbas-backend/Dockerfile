FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for SQLite DB (mount a volume here in production)
RUN mkdir -p /data

# Expose port
EXPOSE 8000

# Default command — PORT env var is overridden by Railway/cloud providers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
