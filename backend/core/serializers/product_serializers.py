from rest_framework import serializers
from core.models import Category, GenericProduct, ProductVariant, Supermarket

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class GenericProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')  

    class Meta:
        model = GenericProduct
        fields = ['id', 'name', 'amount', 'unit', 'category']     



class ProductVariantSerializer(serializers.ModelSerializer):
    supermarket = serializers.CharField(source='supermarket.name')  # readable name
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['variant_name', 'price', 'supermarket', 'image_url', 'last_updated']
        extra_kwargs = {
            'variant_name': {'source': 'name'}
        }

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None           