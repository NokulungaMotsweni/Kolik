from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                     # Admin panel
    path('api/auth/', include('users.urls')),            # User-related endpoints
    path('api/products/', include('products.urls')),     # Product browsing/comparison
    path('api/cart/', include('shopping_cart.urls')),    # Basket handling (will evolve)
]

# Media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)