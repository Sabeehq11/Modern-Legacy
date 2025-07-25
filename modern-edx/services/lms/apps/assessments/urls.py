"""
URL configuration for assessments app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'assessments'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    # API views
    path('api/', include(router.urls)),
]
