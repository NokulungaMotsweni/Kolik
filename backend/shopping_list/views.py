"""
API view for calculating total basket cost per supermarket.

This endpoint accepts a list of products and their quantities,
calculates total prices at different supermarkets, and returns
the cheapest option.

Accessible via:
- GET: Returns usage instructions.
- POST: Processes basket and returns pricing results.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shopping_list.models import ShoppingList
from shopping_list.serializers import BasketSerializer, ShoppingListAddSerializer, ShoppingListRemoveSerializer
from shopping_list.services import analyze_basket_pricing, calculate_totals_for_user, add_to_shopping_list, remove_from_shopping_list, \
    get_shopping_list_basket, get_breakdown_for_supermarket, get_mixed_basket


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
    results, cheapest = analyze_basket_pricing(basket)

    if isinstance(results, dict) and "error" in results:
        return Response(results, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "results": results,
        "cheapest_supermarket": cheapest
    }, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user_shopping_list(request):
    try:
        shopping_list = request.user.shopping_list
    except ShoppingList.DoesNotExist:
        return Response({"error": "Shopping List Not Found."}, status=status.HTTP_404_NOT_FOUND)

    if not shopping_list.items.exists():
        return Response({"message": "Shopping List is Empty."}, status=status.HTTP_204_NO_CONTENT)

    items = []
    for item in shopping_list.items.select_related("product", "variant", "variant__supermarket"):
        items.append({
            "product_name": item.product.name,
            "variant_name": item.variant.name if item.variant else "Flexible (any variant)",
            "supermarket": item.variant.supermarket.name if item.variant and item.variant.supermarket else "Any",
            "quantity": float(item.quantity)
        })

    return Response({"shopping_list": items}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def compare_user_shopping_list(request):
    """
    Compare prices using the logged-in user's saved cart.
    """
    result = calculate_totals_for_user(request.user)

    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    error = result.get("error")
    if error == "Cart is empty.":
        return Response({"message": "Cart is empty."}, status=status.HTTP_204_NO_CONTENT)

    return Response({
        "supermarket_totals": result.get("supermarket_totals", [])
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def view_supermarket_breakdown(request):
    basket = request.data.get("basket")
    supermarket = request.data.get("supermarket")

    if not supermarket:
        return Response({"error": "Supermarket name is required."}, status=400)

    # If basket is not provided, use the logged-in user's shopping_list
    if not basket:
        try:
            shopping_list = request.user.shopping_list
        except ShoppingList.DoesNotExist:
            return Response({"error": "Cart not found."}, status=404)

        basket = [
            {"product_id": item.product.id, "quantity": item.quantity}
            for item in shopping_list.items.all()
        ]

    if not basket:
        return Response({"message": "Cart is empty."}, status=204)

    print("Basket Input:", basket) # Terminal Debugging
    breakdown, full_pricing = get_breakdown_for_supermarket(basket, supermarket)
    print("Breakdown Result:", breakdown) # Terminal Debugging

    if breakdown is None:
        return Response(
            {"error": f"'{supermarket}' was not found in the comparison results."},
            status=status.HTTP_404_NOT_FOUND
        )

    response = {
        "breakdown": breakdown
    }

    warnings = full_pricing.get("warnings", [])
    missing_per_supermarket = full_pricing.get("missing_per_supermarket", {})

    # Only include meta if there's relevant extra info
    if warnings or missing_per_supermarket:
        response["meta"] = {}

        # Include ONLY the requested supermarket in totals
        if full_pricing.get("supermarket_totals"):
            filtered_totals = [
                s for s in full_pricing["supermarket_totals"]
                if s["supermarket"] == supermarket
            ]
            if filtered_totals:
                response["meta"]["supermarket_totals"] = filtered_totals

        if warnings:
            response["meta"]["warnings"] = warnings

        if missing_per_supermarket:
            response["meta"]["missing_per_supermarket"] = {
                k: v for k, v in missing_per_supermarket.items()
                if k == supermarket and v  # non-empty
            }

    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mixed_basket_view(request):
    """
    Return a mixed basket made of the cheapest available variants per product
    in the user's saved cart.
    """
    basket, error = get_shopping_list_basket(request.user)

    if error == "Cart not found.":
        return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)

    if not basket:
        return Response({"message": "Cart is empty."}, status=status.HTTP_204_NO_CONTENT)

    mixed_basket = get_mixed_basket(basket)

    return Response(mixed_basket, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_shopping_list_view(request):
    serializer = ShoppingListAddSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        variant_id = serializer.validated_data.get("variant_id")

        item = add_to_shopping_list(request.user, product_id, quantity, variant_id)

        return Response({
            "message": "Item added to cart.",
            "product": item.product.name,
            "variant": item.variant.name if item.variant else None,
            "quantity": item.quantity,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_shopping_list_view(request):
    serializer = ShoppingListRemoveSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data["product_id"]
        removed = remove_from_shopping_list(request.user, product_id)
        if removed:
            return Response({"message": "Item removed from cart."})
        else:
            return Response({"message": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_shopping_list_view(request):
    try:
        cart = request.user.shopping_list

        print("🧺 Clearing cart for user:", request.user.id)
        print("📦 Cart ID:", cart.id)
        print("🔢 Items before:", cart.items.count())

        deleted, _ = cart.items.all().delete()
        print("✅ Items deleted:", deleted)
        print("🔢 Items after:", cart.items.count())

        return Response({"message": f"Cart cleared. {deleted} item(s) removed."}, status=200)
    except ShoppingList.DoesNotExist:
        return Response({"message": "Cart is already empty."}, status=204)

    print("Cart ID:", cart.id)
    print("Items before:", cart.items.count())
    deleted, _ = cart.items.all().delete()
    print("Items deleted:", deleted)
