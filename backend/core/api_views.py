from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import GenericProduct, ProductVariant
from core.models import Category
from decimal import Decimal

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

# View 6: All generic products are listed (for search or full display)
@api_view(['GET'])
def list_all_products(request):
    products = GenericProduct.objects.select_related('category').all()
    data = []

    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "amount": float(product.amount),
            "unit": product.unit,
            "category": product.category.name,
        })

    return Response(data)




# View 7 - Cheapest basket total across supermarkets
@api_view(['GET', 'POST'])
def calculate_basket(request):
    if request.method == 'GET':
        return Response({
            "example": {
                "basket": [
                    {"product_id": 1, "quantity": 2},  # e.g. 2x 1L milk
                    {"product_id": 3, "quantity": 1}   # e.g. 1x 10-egg carton
                ]
            },
            "instructions": "Send a POST request to this endpoint with JSON like the above to calculate the basket price at each supermarket."
        })

    
    basket = request.data.get("basket", [])
    if not basket:
        return Response({"error": "Basket is empty or missing."}, status=400)

    supermarket_totals = {}  # e.g. { 'Tesco': 97.80, 'Albert': 102.90 }

    # We go through each product in basket
    for item in basket:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)  # default = 1

        try:
            product = GenericProduct.objects.get(id=product_id)
            variants = ProductVariant.objects.filter(generic_product=product)

            # We find the cheapest variant per supermarket
            cheapest_by_supermarket = {}
            for variant in variants:
                market = variant.supermarket.name
                price = Decimal(variant.price)

                # We save the cheapest variant per supermarket
                if market not in cheapest_by_supermarket or price < cheapest_by_supermarket[market].price:
                    cheapest_by_supermarket[market] = variant

            # We add product cost to each supermarket's total
            for market, variant in cheapest_by_supermarket.items():
                price = Decimal(variant.price) * Decimal(quantity)

                if market not in supermarket_totals:
                    supermarket_totals[market] = Decimal("0.0")

                supermarket_totals[market] += price

        except GenericProduct.DoesNotExist:
            return Response({"error": f"Product with ID {product_id} not found."}, status=404)

    # Total is rounded to 2 decimal places
    for market in supermarket_totals:
        supermarket_totals[market] = round(supermarket_totals[market], 2)

    return Response(supermarket_totals)