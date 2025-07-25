"""
URL configuration for content app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'content'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
