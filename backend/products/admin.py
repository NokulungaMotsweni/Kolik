from django.contrib import admin
from products.models import Category, GenericProduct, Supermarket, ProductVariant

admin.site.register(Category)
admin.site.register(GenericProduct)
admin.site.register(Supermarket)
admin.site.register(ProductVariant)