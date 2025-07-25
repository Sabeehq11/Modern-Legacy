"""
Health check URLs for Modern edX CMS.
"""
from django.urls import path
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Basic health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'cms',
        'version': '1.0.0'
    })

def health_detailed(request):
    """Detailed health check with database and cache status."""
    status = {'status': 'healthy', 'checks': {}}
    
    # Database check
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        status['checks']['database'] = 'healthy'
    except Exception as e:
        status['checks']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Cache check
    try:
        cache.set('health_check', 'test', 1)
        cache.get('health_check')
        status['checks']['cache'] = 'healthy'
    except Exception as e:
        status['checks']['cache'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    return JsonResponse(status)

urlpatterns = [
    path('', health_check, name='health_check'),
    path('detailed/', health_detailed, name='health_detailed'),
]
