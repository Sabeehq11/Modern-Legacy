"""
URL configuration for Modern edX CMS.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# Create a router for API endpoints
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('tinymce/', include('tinymce.urls')),
    
    # CMS App URLs
    path('content/', include('apps.content.urls')),
    path('authoring/', include('apps.authoring.urls')),
    path('publishing/', include('apps.publishing.urls')),
    
    # Health check endpoint
    path('health/', include('cms.health_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Modern edX CMS Administration"
admin.site.site_title = "Modern edX CMS Admin"
admin.site.index_title = "Welcome to Modern edX CMS Administration"
