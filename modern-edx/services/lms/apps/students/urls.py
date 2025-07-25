"""
URL configuration for students app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'students'

# Create router for API views
router = DefaultRouter()

urlpatterns = [
    # Web views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('achievements/', views.achievements_view, name='achievements'),
    
    # API views
    path('api/', include(router.urls)),
]
