"""
Production settings for Modern edX LMS.
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Media files should be served by CDN in production
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='modern-edx-media')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Use S3 for media files if AWS credentials are provided
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

# Use WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging for production
LOGGING['handlers']['file']['filename'] = '/var/log/lms/lms.log'

# Email settings for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Disable CORS for all origins in production
CORS_ALLOW_ALL_ORIGINS = False

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 60

# Cache timeout settings
CACHES['default']['TIMEOUT'] = 300  # 5 minutes
