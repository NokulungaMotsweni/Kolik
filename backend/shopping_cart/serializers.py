from rest_framework import serializers

class BasketItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class BasketSerializer(serializers.Serializer):
    basket = BasketItemSerializer(many=True)

    def validate_basket(self, value):
        if not value:
            raise serializers.ValidationError("Basket cannot be empty.")
        return value