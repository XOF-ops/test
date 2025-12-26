# Dockerfile for Master_Brain Agent API
# Part of autonomous research & development protocol infrastructure

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent/ ./agent/
COPY copilot/ ./copilot/

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=agent.api.server
ENV DB_HOST=postgres
ENV DB_NAME=master_brain
ENV DB_USER=master_brain_user
ENV DB_PASSWORD=master_brain_secure_password

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health').raise_for_status()"

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "agent.api.server:app"]
