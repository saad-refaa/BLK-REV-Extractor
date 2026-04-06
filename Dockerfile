# Dockerfile for BLK-REV Extractor
FROM python:3.10-slim

LABEL maintainer="support@blk-rev-extractor.com"
LABEL version="1.0.0"
LABEL description="BLK-REV Extractor Pro - Data extraction tool"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data
RUN mkdir -p /data/input /data/output /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BLK_REV_DATA_DIR=/data

# Default command
CMD ["python", "cli.py", "--help"]

# Entry point for CLI
ENTRYPOINT ["python", "cli.py"]
