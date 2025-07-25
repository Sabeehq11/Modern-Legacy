"""
URL configuration for Modern edX LMS.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views

# Create a router for API endpoints
router = routers.DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),
    path('api/info/', views.api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # LMS App URLs
    path('courses/', include('apps.courses.urls')),
    path('students/', include('apps.students.urls')),
    path('instructors/', include('apps.instructors.urls')),
    path('assessments/', include('apps.assessments.urls')),
    
    # Health check endpoint
    path('health/', include('lms.health_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Modern edX LMS Administration"
admin.site.site_title = "Modern edX LMS Admin"
admin.site.index_title = "Welcome to Modern edX LMS Administration"
