from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import GenericProduct, ProductVariant, Category
from decimal import Decimal
from core.services.basket_service import calculate_total_per_supermarket
from core.serializers.product_serializers import (
    CategorySerializer,
    GenericProductSerializer,
    ProductVariantSerializer
)

# View 1: Returns the cheapest variant for a given generic product (by ID)
@api_view(['GET'])
def best_deal_by_id(request, product_id):
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found."}, status=404)

        best_variant = min(variants, key=lambda x: x.price)
        serializer = ProductVariantSerializer(best_variant, context={"request": request})

        return Response({
            "product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "best_variant": serializer.data
        })
    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

# View 2: Lists all variants available for a specific generic product
@api_view(['GET'])
def all_variants_by_product(request, product_id):
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found for this product."}, status=404)

        serializer = ProductVariantSerializer(variants, many=True, context={"request": request})

        return Response({
            "generic_product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "variants": serializer.data
        })
    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

# View 3: Lists all product categories (e.g., Dairy, Bakery)
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# View 4: Lists all generic products inside a specific category
@api_view(['GET'])
def products_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = GenericProduct.objects.filter(category=category)
        serializer = GenericProductSerializer(products, many=True)

        return Response({
            "category": category.name,
            "products": serializer.data
        })
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)

# View 5: Lists all generic products (for browsing or search results)
@api_view(['GET'])
def list_all_products(request):
    products = GenericProduct.objects.select_related('category').all()
    serializer = GenericProductSerializer(products, many=True)
    return Response(serializer.data)

# View 6: Delegates basket calculation to a service.
# Calculates total price of a user's basket across all supermarkets
# using the cheapest available variant per product.
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

# TODO:
# - Add BasketSerializer to validate basket structure (product_id + quantity)
# - Optional: Save basket for authenticated users
# - Optional: Cache basket prices for repeated queries