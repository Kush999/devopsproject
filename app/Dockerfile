FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install build dependencies required for psutil and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variable
ENV ENVIRONMENT=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check built into Docker
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the app
CMD ["python", "app.py"]
