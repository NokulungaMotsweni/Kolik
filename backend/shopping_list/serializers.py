from rest_framework import serializers

# For /list/calculate/ (stateless pricing)
class BasketItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class BasketSerializer(serializers.Serializer):
    basket = BasketItemSerializer(many=True)

    def validate_basket(self, value):
        if not value:
            raise serializers.ValidationError("Basket cannot be empty.")
        return value

# for /list/add/
class ShoppingListAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    variant_id = serializers.IntegerField(required=False, allow_null=True)

class ShoppingListRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()