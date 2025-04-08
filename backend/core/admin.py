from django.contrib import admin
from .models import Category, GenericProduct, Supermarket, ProductVariant

# This makes the models show up in the Django admin panel
admin.site.register(Category)
admin.site.register(GenericProduct)
admin.site.register(Supermarket)
admin.site.register(ProductVariant)