"""
Production settings for Modern edX CMS.
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
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Disable browsable API in production
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

# Static files handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Disable debug toolbar and other development tools
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ['django_extensions']]

# More restrictive CORS in production
CORS_ALLOW_ALL_ORIGINS = False

# Production logging
LOGGING['handlers']['file']['filename'] = '/var/log/cms/cms.log'
