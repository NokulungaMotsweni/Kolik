"""
API view for calculating total basket cost per supermarket.

This endpoint accepts a list of products and their quantities,
calculates total prices at different supermarkets, and returns
the cheapest option.

Accessible via:
- GET: Returns usage instructions.
- POST: Processes basket and returns pricing results.
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
            "instructions": "Send a POST request with JSON like the example to calculate your basket price."
        })

    # Validate basket structure
    serializer = BasketSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    basket = serializer.validated_data["basket"]

    # Perform pricing calculation
    results, cheapest = calculate_total_per_supermarket(basket)

    if isinstance(results, dict) and "error" in results:
        return Response(results, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "results": results,
        "cheapest_supermarket": cheapest
    }, status=status.HTTP_200_OK)