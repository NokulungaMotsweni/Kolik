"""
Registers product-related models with the Django admin interface.

This allows admins to view, add, edit, and delete:
- Product categories
- Generic products (e.g., "Milk 1L")
- Supermarkets (e.g., Tesco, Billa)
- Product variants (specific brands in shops)
"""

from django.contrib import admin
from products.models import Category, GenericProduct, Supermarket, ProductVariant

admin.site.register(Category)
admin.site.register(GenericProduct)
admin.site.register(Supermarket)
admin.site.register(ProductVariant)