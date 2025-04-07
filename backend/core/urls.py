from django.urls import path
from . import api_views

urlpatterns = [
    path('best-deal/<int:product_id>/', api_views.best_deal_by_id, name='best_deal_by_id'),
    path('all-variants/<int:product_id>/', api_views.all_variants_by_product, name='all_variants'),
]