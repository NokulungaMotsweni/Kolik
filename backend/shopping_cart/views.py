"""
API views for the 'shopping_cart' app.

This module provides a single endpoint for:
- Accepting a user's basket (list of product IDs and quantities)
- Calculating total cost per supermarket
- Identifying the cheapest option

Accessible via both GET (instructions) and POST (calculation).
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from shopping_cart.serializers import BasketSerializer
from shopping_cart.services import calculate_total_per_supermarket

@api_view(['GET', 'POST'])
def calculate_basket(request):
    if request.method == 'GET':
        return Response({
            "example": {
                "basket": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 3, "quantity": 1}
                ]
            },
            "instructions": "Send a POST request to this endpoint with JSON like the above to calculate basket price."
        })

    # VALIDATION with BasketSerializer
    serializer = BasketSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    basket = serializer.validated_data["basket"]

    # Business logic
    results, cheapest = calculate_total_per_supermarket(basket)

    if isinstance(results, dict) and "error" in results:
        return Response(results, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "results": results,
        "cheapest_supermarket": cheapest
    })