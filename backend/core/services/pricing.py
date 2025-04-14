def get_best_variant(variants):
    """
    Returns the product variant with the lowest price.
    
    """
    if not variants:
        return None
    return min(variants, key=lambda x: x.price)