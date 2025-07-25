"""
URL configuration for courses app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'courses'

# Create router for API views
router = DefaultRouter()
router.register(r'', views.CourseViewSet, basename='course')

urlpatterns = [
    # Web views
    path('', views.course_catalog, name='catalog'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<str:course_id>/', views.course_detail, name='detail'),
    path('<str:course_id>/progress/', views.course_progress, name='progress'),
    
    # API views
    path('api/', include(router.urls)),
]
