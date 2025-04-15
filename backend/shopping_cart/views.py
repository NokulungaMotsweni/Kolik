from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

    basket = request.data.get("basket", [])
    if not basket:
        return Response({"error": "Basket is empty or missing."}, status=400)

    results, cheapest = calculate_total_per_supermarket(basket)

    if isinstance(results, dict) and "error" in results:
        return Response(results, status=404)

    return Response({
        "results": results,
        "cheapest_supermarket": cheapest
    })
