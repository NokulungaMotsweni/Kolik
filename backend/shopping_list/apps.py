from django.apps import AppConfig


class ShoppingCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping_list'


#defines how Django initializes the shopping_list app
