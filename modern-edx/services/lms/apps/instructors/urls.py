"""
URL configuration for instructors app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'instructors'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    # API views
    path('api/', include(router.urls)),
]
