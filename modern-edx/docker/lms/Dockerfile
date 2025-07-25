FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=lms.settings.production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        build-essential \
        libpq-dev \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        libwebp-dev \
        zlib1g-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY services/lms/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY services/lms/ .
COPY services/shared/ ./shared/

# Create necessary directories
RUN mkdir -p logs staticfiles media

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput --settings=lms.settings.development

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "lms.wsgi:application"]
