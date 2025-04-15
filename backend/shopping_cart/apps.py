from django.apps import AppConfig


class ShoppingCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping_cart'


#defines how Django initializes the shopping_cart app        
