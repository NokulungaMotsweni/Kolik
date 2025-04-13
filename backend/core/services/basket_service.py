from decimal import Decimal
from core.models import GenericProduct, ProductVariant

def calculate_total_per_supermarket(basket):
    """
    Calculates basket total per supermarket using cheapest variants.
    Returns (results, cheapest_supermarket) or ({"error": str}, None)
    """
    supermarket_totals = {}

    for item in basket:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        try:
            product = GenericProduct.objects.get(id=product_id)
        except GenericProduct.DoesNotExist:
            return {"error": f"Product with ID {product_id} not found."}, None

        variants = ProductVariant.objects.filter(generic_product=product)
        if not variants.exists():
            continue

        cheapest_by_market = {}
        for variant in variants:
            market = variant.supermarket.name
            price = Decimal(variant.price)

            if market not in cheapest_by_market or price < cheapest_by_market[market].price:
                cheapest_by_market[market] = variant

        for market, variant in cheapest_by_market.items():
            price = Decimal(variant.price) * Decimal(quantity)
            supermarket_totals[market] = supermarket_totals.get(market, Decimal("0.0")) + price

    results = [{"supermarket": market, "total": round(total, 2)} for market, total in supermarket_totals.items()]
    cheapest = min(results, key=lambda x: x["total"]) if results else None

    return results, cheapest