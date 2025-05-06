"""
URL patterns for the 'products' app.

These endpoints allow users to:
- Browse product categories
- View all generic products
- Search for products
- View all variants of a product
- Find the best deal (cheapest offer) for a specific product
"""

from django.urls import path
from products import views  


urlpatterns = [
    path("best-deal/<int:product_id>/", views.best_deal_by_id),
    path("all-variants/<int:product_id>/", views.all_variants_by_product),
    path("categories/", views.list_categories),
    path("products-by-category/<int:category_id>/", views.products_by_category),
    path("all-products/", views.list_all_products),
    path("search/", views.search_products),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
]