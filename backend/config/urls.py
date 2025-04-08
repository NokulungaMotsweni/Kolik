from django.contrib import admin
from django.urls import path, include  # Used to include app-level URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                     # Admin panel at /admin/
    path('api/', include('core.urls')),                  # All API routes are handled in core/urls.py
]

# This enables serving uploaded media files (like product images) in development
# In production, media will be handled differently 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)