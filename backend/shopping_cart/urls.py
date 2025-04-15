from django.urls import path
from .views import calculate_basket

urlpatterns = [
    path("basket/", calculate_basket),
]