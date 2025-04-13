from django.urls import path
from core.views import product_views  

urlpatterns = [
    path('best-deal/<int:product_id>/', product_views.best_deal_by_id),
    path('all-variants/<int:product_id>/', product_views.all_variants_by_product),
    path('categories/', product_views.list_categories),
    path('products-by-category/<int:category_id>/', product_views.products_by_category),
    path('products/', product_views.list_all_products),
    path('basket/', product_views.calculate_basket),
]