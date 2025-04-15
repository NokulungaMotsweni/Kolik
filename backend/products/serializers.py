"""
Serializers for the 'products' app.

These classes define how product-related models are converted to JSON
for API responses, and how incoming data is validated when creating or updating.

Included serializers:
- CategorySerializer: Returns product category info
- GenericProductSerializer: Shows generic products users compare
- ProductVariantSerializer: Shows specific product offers in supermarkets
"""

from rest_framework import serializers
from products.models import Category, GenericProduct, ProductVariant, Supermarket


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes product categories (e.g., Dairy, Bakery).
    """
    class Meta:
        model = Category
        fields = ['id', 'name']


class GenericProductSerializer(serializers.ModelSerializer):
    """
    Serializes a generic product like 'Whole Milk 1L'.
    Returns the product name, amount, unit, and the category name.
    """
    category = serializers.CharField(source='category.name')  # Shows just the category name (not full object)

    class Meta:
        model = GenericProduct
        fields = ['id', 'name', 'amount', 'unit', 'category']


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializes specific supermarket product variants (e.g., 'Olma milk at Tesco').
    Includes product name, price, store, image, and last updated time.
    """
    supermarket = serializers.CharField(source='supermarket.name')  # Displays readable supermarket name
    image_url = serializers.SerializerMethodField()  # Custom logic to build image URL

    class Meta:
        model = ProductVariant
        fields = ['variant_name', 'price', 'supermarket', 'image_url', 'last_updated']
        extra_kwargs = {
            'variant_name': {'source': 'name'}  # Maps 'name' to 'variant_name' in the API
        }

    def get_image_url(self, obj):
        """
        Returns the absolute URL of the product image, if available.
        """
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None