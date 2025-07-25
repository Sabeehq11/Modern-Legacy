"""
URL configuration for publishing app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'publishing'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
