from collections import defaultdict
from decimal import Decimal
from itertools import product

from rest_framework.generics import get_object_or_404

from products.models import GenericProduct, ProductVariant
from .models import ShoppingList, ShoppingListItem


def analyze_basket_pricing(basket):
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
    supermarket_names = set()
    product_breakdown = []
    mixed_basket_items = []
    supermarket_totals = {}
    supermarket_totals_list = []
    mixed_total = Decimal("0.0")
    warnings = []

    combined = defaultdict(Decimal)
    for item in basket:
        pid = item["product_id"]
        qty = Decimal(item.get("quantity", 1))
        combined[pid] += qty

    basket = [{"product_id": pid, "quantity": qty} for pid, qty in combined.items()]

    # Preload all variants
    all_variants = ProductVariant.objects.select_related("supermarket", "generic_product")

    for item in basket:
        try:
            generic_product = GenericProduct.objects.get(id=item['product_id'])
        except GenericProduct.DoesNotExist:
            warnings.append(f"Product {item['product_id']} not found.")
            continue

        quantity = Decimal(item.get("quantity", 1))
        variants = all_variants.filter(generic_product=generic_product)

        if not variants.exists():
            warnings.append(f"No variants available for '{generic_product.name}'.")
            continue

        # Organize prices by supermarket for this product
        product_row = {
            "product": generic_product.name,
            "quantity": quantity,
            "supermarkets": [],
            "best_price": None,
            "best_supermarket": None
        }

        cheapest_variant = None

        for variant in variants:
            supermarket_name = variant.supermarket.name
            price = Decimal(variant.price)
            total = price * quantity

            # Track all supermarkets
            supermarket_names.add(supermarket_name)

            product_row["supermarkets"].append({
                "name": supermarket_name,
                "price": price,
                "total": total,
                "variant": variant.name
            })

            # Track the  best variant (for mixed basket)
            if not cheapest_variant or price < cheapest_variant.price:
                cheapest_variant = variant

            # Add to per-supermarket totals
            if supermarket_name not in supermarket_totals:
                supermarket_totals[supermarket_name] = {"total": Decimal("0.0"), "all_items_available": True}
            supermarket_totals[supermarket_name]["total"] += total

            # Fill in missing stores with nulls
            existing = {s["name"] for s in product_row["supermarkets"]}
            for market in supermarket_totals:
                if market not in existing:
                    product_row["supermarkets"].append({
                        "name": market,
                        "price": None,
                        "total": None,
                        "variant": None
                    })
                    supermarket_totals[market]["all_items_available"] = False

        if cheapest_variant:
            product_row["best_price"] = float(cheapest_variant.price)
            product_row["best_supermarket"] = cheapest_variant.supermarket.name
            mixed_basket_items.append({
                "product": generic_product.name,
                "variant": cheapest_variant.name,
                "supermarket": cheapest_variant.supermarket.name,
                "price": cheapest_variant.price,
                "quantity": quantity,
                "total": cheapest_variant.price * quantity
            })

        product_breakdown.append(product_row)

    # Prepare final results
    for name in sorted(supermarket_totals.keys()):
        total_data = supermarket_totals[name]
        supermarket_totals_list.append({
            "supermarket": name,
            "total": total_data.get("total", 0.0),
            "all_items_available": total_data.get("all_items_available", False)
        })

    mixed_total = sum(item["total"] for item in mixed_basket_items)

    return {
        "products": product_breakdown,
        "supermarket_totals": [
            {
                "supermarket": st["supermarket"],
                "total": float(round(Decimal(st["total"]), 2)),
                "all_items_available": st["all_items_available"]
            }
            for st in supermarket_totals_list
        ],
        "best_mixed_basket": {
            "total": float(round(mixed_total, 2)),
            "items": [
                {
                    **item,
                    "price": float(round(item["price"], 2)),
                    "quantity": float(item["quantity"]),
                    "total": float(round(item["total"], 2)),
                }
                for item in mixed_basket_items
            ]
        },
        "warnings": warnings
    }


def calculate_totals_for_user(user):
    """
    Load the user's cart and run total calculations.
    """
    try:
        cart = ShoppingList.objects.get(user=user)
    except ShoppingList.DoesNotExist:
        return {
            "products": [],
            "supermarket_totals": [],
            "best_mixed_basket": {
                "total": 0.0,
                "items": []
            },
            "warnings": [],
            "error": "Cart not found."
        }

    basket = [
        {"product_id": item.product.id, "quantity": item.quantity}
        for item in cart.items.all()
    ]

    if not basket:
        return {
            "products": [],
            "supermarket_totals": [],
            "best_mixed_basket": {
                "total": 0.0,
                "items": []
            },
            "warnings": [],
            "error": "Cart is empty."
        }

    return analyze_basket_pricing(basket)


def compare_supermarkets(basket):
    result = analyze_basket_pricing(basket)

    if isinstance(result, tuple):
        data, _ = result  # first item is the data dict
    else:
        data = result

    return data.get("supermarket_totals", [])


def find_cheapest_supermarket(supermarket_totals):
    available = [s for s in supermarket_totals if s["all_items_available"]]
    best = min(available, key=lambda s: s["total"]) if available else None
    return {"name": best["supermarket"], "total": best["total"]} if best else None


def get_mixed_basket(basket):
    result = analyze_basket_pricing(basket)
    return result.get("best_mixed_basket", {})


def add_to_shopping_list(user, product_id, quantity, variant_id=None):
    """
    Adds a product to the user's cart.
    """
    # Get or create the user's shopping cart
    cart, _ = ShoppingList.objects.get_or_create(user=user)

    # Get the product
    product = get_object_or_404(GenericProduct, id=product_id)

    # Get the variant only if one is specified
    variant = None
    if variant_id is not None:
        variant = get_object_or_404(ProductVariant, id=variant_id)

    # Define unique lookup based on locked flag
    lookup = {
        "cart": cart,
        "product": product,
        "variant": variant,
    }

    # Add or update the cart item
    item, created = ShoppingListItem.objects.update_or_create(
        **lookup,
        defaults={"quantity": quantity}
    )

    return item


def remove_from_shopping_list(user, product_id):
    try:
        cart, _ = ShoppingList.objects.get_or_create(user=user)
        product = get_object_or_404(GenericProduct, id=product_id)
        deleted, _ = ShoppingListItem.objects.filter(cart=cart, product=product).delete()
        return deleted > 0
    except ShoppingList.DoesNotExist:
        return False


def get_shopping_list_basket(user):
    try:
        cart = ShoppingList.objects.get(user=user)
    except ShoppingList.DoesNotExist:
        return [], "Cart not found."

    items = [
        {
            "product_id": item.product.id,
            "quantity": item.quantity
        }
        for item in cart.items.all()
    ]

    return items, None

    #     # Validate product existence
    #     try:
    #         product = GenericProduct.objects.get(id=product_id)
    #     except GenericProduct.DoesNotExist:
    #         return {"error": f"Product with ID {product_id} not found."}, None
    #
    #     # Get all available variants for the product
    #     variants = ProductVariant.objects.filter(generic_product=product)
    #     if not variants.exists():
    #         continue  # Skip if no offers available
    #
    #     # Find the cheapest variant per supermarket
    #     cheapest_by_market = {}
    #     for variant in variants:
    #         market = variant.supermarket.name  # ✅ FIXED here
    #         price = Decimal(variant.price)
    #
    #         if market not in cheapest_by_market or price < cheapest_by_market[market].price:
    #             cheapest_by_market[market] = variant
    #
    #     # Add the price for this product (x quantity) to each supermarket total
    #     for market, variant in cheapest_by_market.items():
    #         price = Decimal(variant.price) * Decimal(quantity)
    #         supermarket_totals[market] = supermarket_totals.get(market, Decimal("0.0")) + price
    #
    # # Format results: list of totals per supermarket
    # results = [{"supermarket": market, "total": round(total, 2)} for market, total in supermarket_totals.items()]
    # cheapest = min(results, key=lambda x: x["total"]) if results else None
    #
    # return results, cheapest


def get_breakdown_for_supermarket(basket, supermarket_name):
    results = analyze_basket_pricing(basket)

    if not isinstance(results, dict) or "supermarket_totals" not in results:
        return None, results

    store_data = next((s for s in results["supermarket_totals"]
                       if s["supermarket"] == supermarket_name), None)
    if not store_data:
        return None, results

    store_items = []
    for p in results["products"]:
        match = next((s for s in p["supermarkets"]
                      if s["name"] == supermarket_name), None)

        if match and isinstance(match.get("price"), (int, float)) and isinstance(match.get("total"), (int, float)):
            store_items.append({
                "product": p["product"],
                "variant": match["variant"],
                "price": float(match["price"]),
                "quantity": float(p["quantity"]),
                "total": float(match["total"])
            })

    # Sort alphabetically by product name
    store_items.sort(key=lambda x: x["product"])

    # Collect missing items
    missing_items = []
    for product in results["products"]:
        found = False
        for store in product.get("supermarkets", []):
            if store["name"] == supermarket_name and store["price"] is not None:
                found = True
                break
        if not found:
            missing_items.append(product["product"])

    # ✅ Recalculate total from matched items
    calculated_total = float(round(sum(item["total"] for item in store_items if item["total"] is not None), 2))

    # ✅ Patch the meta totals so it reflects the accurate total for this supermarket
    adjusted_meta = []
    for s in results["supermarket_totals"]:
        if s["supermarket"] == supermarket_name:
            adjusted_total = calculated_total
        else:
            adjusted_total = s.get("total")
            if adjusted_total is not None:
                adjusted_total = float(round(adjusted_total, 2))

        adjusted_meta.append({
            "supermarket": s["supermarket"],
            "total": adjusted_total,
            "all_items_available": s.get("all_items_available", False)
        })

    return {
        "supermarket": supermarket_name,
        "total": calculated_total,
        "items": store_items,
        "unavailable_items": missing_items
    }, {
        "supermarket_totals": adjusted_meta,
        "warnings": results.get("warnings", [])
    }
