from django.urls import path
from .api_views import (
    best_deal_by_id,
    all_variants_by_product,
    list_categories,
    products_by_category,
)

urlpatterns = [
    path('best-deal/<int:product_id>/', best_deal_by_id),
    path('all-variants/<int:product_id>/', all_variants_by_product),
    path('categories/', list_categories),
    path('products-by-category/<int:category_id>/', products_by_category),
]