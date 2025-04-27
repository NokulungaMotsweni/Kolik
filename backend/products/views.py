"""
API views for the 'products' app.

This module provides read-only endpoints for:
- Viewing product categories
- Viewing generic products and their supermarket variants
- Comparing prices across supermarkets
- Searching for products

These views are designed for public access and do not require authentication.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import GenericProduct, ProductVariant, Category
from products.services import get_best_variant 
from products.serializers import (
    CategorySerializer,
    GenericProductSerializer,
    ProductVariantSerializer
)


# View 1: Get the best (cheapest) variant for a given generic product

@api_view(['GET'])
def best_deal_by_id(request, product_id):
    """
    Returns the cheapest available variant of a specific generic product.

    Args:
        product_id (int): The ID of the generic product to compare.

    Returns:
        JSON containing product info and the best (lowest price) variant.
    """
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found."}, status=404)

        best_variant = get_best_variant(variants)
        serializer = ProductVariantSerializer(best_variant, context={"request": request})

        return Response({
            "product": product.cookie_name,
            "amount": product.amount,
            "unit": product.unit,
            "best_variant": serializer.data
        })
    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)


# View 2: List all variants for a specific generic product

@api_view(['GET'])
def all_variants_by_product(request, product_id):
    """
    Returns all supermarket variants for a given generic product.

    Args:
        product_id (int): The ID of the generic product.

    Returns:
        JSON with the list of all product variants available.
    """
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found for this product."}, status=404)

        serializer = ProductVariantSerializer(variants, many=True, context={"request": request})

        return Response({
            "generic_product": product.cookie_name,
            "amount": product.amount,
            "unit": product.unit,
            "variants": serializer.data
        })
    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)


# View 3: List all product categories

@api_view(['GET'])
def list_categories(request):
    """
    Returns a list of all available product categories.

    Example: Dairy, Bakery, Vegetables, etc.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# View 4: List all generic products in a category

@api_view(['GET'])
def products_by_category(request, category_id):
    """
    Returns all generic products that belong to a specific category.

    Args:
        category_id (int): ID of the category.

    Returns:
        JSON with the category name and products inside it.
    """
    try:
        category = Category.objects.get(id=category_id)
        products = GenericProduct.objects.filter(category=category)
        serializer = GenericProductSerializer(products, many=True)

        return Response({
            "category": category.cookie_name,
            "products": serializer.data
        })
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)


# View 5: List all generic products

@api_view(['GET'])
def list_all_products(request):
    """
    Returns a list of all generic products in the system.

    This is used for general browsing or showing full results.
    """
    products = GenericProduct.objects.select_related('category').all()
    serializer = GenericProductSerializer(products, many=True)
    return Response(serializer.data)


# View 6: Search products by name

@api_view(['GET'])
def search_products(request):
    """
    Searches for generic products by name using a query parameter (?q=milk).

    Returns:
        Matching generic products (case-insensitive search).
    """
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({"error": "Search query cannot be empty."}, status=400)

    results = GenericProduct.objects.filter(name__icontains=query)
    serializer = GenericProductSerializer(results, many=True)
    return Response(serializer.data)


# TODOs (Future Improvements)
# - Add BasketSerializer to validate basket structure (product_id + quantity)
# - Save basket per user (if logged in)
# - Cache basket results for performance

