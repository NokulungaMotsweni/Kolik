from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import GenericProduct, ProductVariant
from core.models import Category

# View 1: Returns the cheapest product variant by product name - OPTIONAL for now second view is more accurate as it relies on ID
@api_view(['GET'])
def best_deal(request, product_name):
    try:
        product = GenericProduct.objects.get(name__iexact=product_name)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found for this product."}, status=404)

        # Find the variant with the lowest price
        best_variant = min(variants, key=lambda x: x.price)

        data = {
            "product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "best_price": float(best_variant.price),
            "supermarket": best_variant.supermarket.name,
            "variant_name": best_variant.name,
        }

        return Response(data)

    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)


# View 2: Returns the best deal using product ID (this one is preferred)
@api_view(['GET'])
def best_deal_by_id(request, product_id):
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found."}, status=404)

        best_variant = min(variants, key=lambda x: x.price)

        return Response({
            "product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "best_price": float(best_variant.price),
            "supermarket": best_variant.supermarket.name,
            "variant_name": best_variant.name,
        })

    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)


# View 3: Returns all available variants for a given product (by ID)
@api_view(['GET'])
def all_variants_by_product(request, product_id):
    try:
        product = GenericProduct.objects.get(id=product_id)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found for this product."}, status=404)

        data = []

        for variant in variants:
            data.append({
                "variant_name": variant.name,
                "price": float(variant.price),
                "supermarket": variant.supermarket.name,
                "image_url": variant.image.url if variant.image else None,
                "last_updated": variant.last_updated.strftime('%Y-%m-%d %H:%M'),
            })

        return Response({
            "generic_product": product.name,
            "amount": product.amount,
            "unit": product.unit,
            "variants": data
        })

    except GenericProduct.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

#  View 4: List all categories (e.g. Dairy, Bakery)
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    data = [{"id": cat.id, "name": cat.name} for cat in categories]
    return Response(data)


# View 5: List all products inside a category
@api_view(['GET'])
def products_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = GenericProduct.objects.filter(category=category)
        data = []

        for product in products:
            data.append({
                "id": product.id,
                "name": product.name,
                "amount": float(product.amount),
                "unit": product.unit
            })

        return Response({
            "category": category.name,
            "products": data
        })

    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)        