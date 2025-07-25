"""
Basic views for Modern edX LMS.
"""
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    """Home page view."""
    context = {
        'title': 'Modern edX LMS',
        'description': 'Welcome to the Modern edX Learning Management System',
        'version': '1.0.0',
        'features': [
            'Modern Django 4.2 architecture',
            'RESTful API design',
            'Microservices ready',
            'Docker containerization',
            'PostgreSQL & Redis support',
            'Comprehensive testing',
        ]
    }
    return render(request, 'home.html', context)

def api_info(request):
    """API information endpoint."""
    return JsonResponse({
        'service': 'Modern edX LMS',
        'version': '1.0.0',
        'api_version': 'v1',
        'endpoints': {
            'health': '/health/',
            'admin': '/admin/',
            'api': '/api/v1/',
            'api_auth': '/api-auth/',
        },
        'status': 'operational'
    })
