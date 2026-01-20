FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for spaCy and transformers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies directly (no venv needed)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm && \
    python -m spacy download de_core_news_sm

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OUTPUT_DIR=/app/output

# Create output directory
RUN mkdir -p /app/output

# Default command (overridden by Dev Container)
CMD ["python", "main.py"]
