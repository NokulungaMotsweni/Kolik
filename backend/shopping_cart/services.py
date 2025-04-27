"""
Business logic for the shopping cart app.

This module contains core price comparison logic:
- Calculates the total basket cost per supermarket
- Uses the cheapest variant of each product in the basket
- Identifies the overall cheapest supermarket
"""

from decimal import Decimal
from products.models import GenericProduct, ProductVariant


def calculate_total_per_supermarket(basket):
    """
    Calculates the total cost of a basket per supermarket, using the cheapest
    available variant of each product.

    Args:
        basket (list): A list of dictionaries in the form:
            [{"product_id": 1, "quantity": 2}, {"product_id": 4, "quantity": 1}, ...]

    Returns:
        tuple:
            - A list of supermarkets and their corresponding total basket prices:
                [{"supermarket": "Tesco", "total": 67.80}, ...]
            - The supermarket with the cheapest total (dict), or None if no matches found.

        If a product in the basket is missing, returns:
            ({"error": str}, None)
    """
    supermarket_totals = {}

    for item in basket:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        # Validate product existence
        try:
            product = GenericProduct.objects.get(id=product_id)
        except GenericProduct.DoesNotExist:
            return {"error": f"Product with ID {product_id} not found."}, None

        # Get all available variants for the product
        variants = ProductVariant.objects.filter(generic_product=product)
        if not variants.exists():
            continue  # Skip if no offers available

        # Find the cheapest variant per supermarket
        cheapest_by_market = {}
        for variant in variants:
            market = variant.supermarket.cookie_name
            price = Decimal(variant.price)

            if market not in cheapest_by_market or price < cheapest_by_market[market].price:
                cheapest_by_market[market] = variant

        # Add the price for this product (x quantity) to each supermarket total
        for market, variant in cheapest_by_market.items():
            price = Decimal(variant.price) * Decimal(quantity)
            supermarket_totals[market] = supermarket_totals.get(market, Decimal("0.0")) + price

    # Format results: list of totals per supermarket
    results = [{"supermarket": market, "total": round(total, 2)} for market, total in supermarket_totals.items()]
    cheapest = min(results, key=lambda x: x["total"]) if results else None

    return results, cheapest