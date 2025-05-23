"""
URL configuration for the Kolik Django project.

This file routes API endpoints and admin interface access.

Routes:
- /admin/ → Django admin panel
- /api/auth/ → User registration and login (handled by `users` app)
- /api/products/ → Product listings and comparisons (handled by `products` app)
- /api/cart/ → Basket and deal logic (handled by `shopping_cart` app)

Note:
In development mode, media files are served using Django’s static file server.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    if getattr(request, 'show_vpn_warning', False):
        return render(request, 'vpn_warning.html')
    return JsonResponse({'message': 'Welcome to Kolik backend'})


urlpatterns = [
    path('admin/', admin.site.urls),                     
    path('api/auth/', include('users.urls')),            
    path('api/products/', include('products.urls')),     
    path('api/cart/', include('shopping_cart.urls')),
    path('', home),
]

# Media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)