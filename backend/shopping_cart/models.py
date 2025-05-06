from django.db import models
from products.models import GenericProduct, ProductVariant


class ShoppingCart(models.Model):
    """
    Represents ab shopping cart that is associated with a single user.

    This models keeps track of the creation and the update times of the cart
    and establishes a one-to-one relationship with the user.
    """

    # Default Moel Manager
    objects = models.Manager()

    # Each user has exactly one shopping cart
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    # Timestamp - When the shopping cart was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp - When the shopping cart was created
    updated_at = models.DateTimeField(auto_now=True)

    def add_item(self, product, variant=None, quantity=1):
        """
        Adds an item to the cart. If it already exists, increase quantity.
        """
        item, created = self.items.get_or_create(
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        return item

    def __str__(self):
        # String representation for admin/shell debugging
        return f"ShoppingCart for {self.user}"



class CartItem(models.Model):
    """
    Represents an item within the user;s shopping cart.

    Each CartItem links to a specific product (and optionally a product variant).
    Tracks the quantity selected by the user.

.    """

    # Default Moel Manager
    objects = models.Manager()

    # Reference to the shopping cart
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # Product added to the cart
    product = models.ForeignKey(GenericProduct, on_delete=models.CASCADE)

    # Opti0nal variant of the product
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Quantity of the product/variant added to the cart
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        # String representation for admin/shell/debugging
        return f"{self.quantity}x {self.product} (Variant: {self.variant}) in cart {self.cart.id}"

# Create your models here.
