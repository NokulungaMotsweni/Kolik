from django.db import models

# CATEGORY: groups generic products like Dairy, Bakery, etc.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"    


# GENERIC PRODUCT: what users compare (e.g. "Full-fat milk 1L")
class GenericProduct(models.Model):
    UNIT_CHOICES = [
        ("L", "Liters"),
        ("ml", "Milliliters"),
        ("g", "Grams"),
        ("kg", "Kilograms"),
        ("pcs", "Pieces"),
        ("ks", "Ks (Czech for 'pieces')"),
    ]

    name = models.CharField(max_length=100)  # e.g., "Full-fat milk"
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)  # dropdown in admin!
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} – {self.amount} {self.unit}"



class Supermarket(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    generic_product = models.ForeignKey(GenericProduct, on_delete=models.CASCADE, related_name='variants')
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # e.g., "Olma Selské mléko plnotučné 3,9%"
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} at {self.supermarket.name} – {self.price} Kč"