from django.urls import path
from .views import calculate_basket, compare_user_shopping_list, add_to_shopping_list_view, remove_from_shopping_list_view, view_user_shopping_list, \
    view_supermarket_breakdown, get_mixed_basket_view, clear_shopping_list_view

urlpatterns = [
    path("view/", view_user_shopping_list, name="view_shopping_list"),
    path("add/", add_to_shopping_list_view, name="add_to_shopping_list"),
    path("remove/", remove_from_shopping_list_view, name="remove_from_shopping_list"),
    path("compare/", compare_user_shopping_list, name="compare_user_shopping_list"),
    path("mixed-basket/", get_mixed_basket_view, name="mixed_basket"),
    path("supermarket-breakdown/", view_supermarket_breakdown, name="supermarket_breakdown"),
    path("basket/", calculate_basket, name="calculate_basket"),  # Optional external analyzer
    path("clear/", clear_shopping_list_view, name="clear_shopping_list"),
]