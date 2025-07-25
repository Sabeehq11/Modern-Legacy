"""
URL configuration for authoring app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'authoring'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
