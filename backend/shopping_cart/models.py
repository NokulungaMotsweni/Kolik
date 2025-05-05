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

    def __str__(self):
        # String representation for admin/shell debugging
        return f"ShoppingCart for {self.user}"




# Create your models here.
