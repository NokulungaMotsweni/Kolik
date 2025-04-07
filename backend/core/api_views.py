from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import GenericProduct, ProductVariant

# 🥇 View 1: Best deal by product name
@api_view(['GET'])
def best_deal(request, product_name):
    try:
        product = GenericProduct.objects.get(name__iexact=product_name)
        variants = ProductVariant.objects.filter(generic_product=product)

        if not variants.exists():
            return Response({"error": "No variants found for this product."}, status=404)

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

# 🥈 View 2: Best deal by product ID (use this one for now!)
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