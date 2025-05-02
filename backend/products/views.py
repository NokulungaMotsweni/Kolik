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
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found."}, status=404)

        best_variant = get_best_variant(variants)
        serializer = ProductVariantSerializer(best_variant, context={"request": request})

        return Response({
            "product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "best_variant": serializer.data
        })
    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)


# View 2: List all variants for a specific generic product
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


# View 3: List all product categories
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# View 4: List all generic products in a category
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


# View 5: List all generic products
@api_view(['GET'])
def list_all_products(request):
    products = GenericProduct.objects.select_related('category').all()
    serializer = GenericProductSerializer(products, many=True)
    return Response(serializer.data)


# View 6: Search products by name
@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({"error": "Search query cannot be empty."}, status=400)

    results = GenericProduct.objects.filter(name__icontains=query)
    serializer = GenericProductSerializer(results, many=True)
    return Response(serializer.data)