from django.db import models

# Category groups products by type (e.g. Dairy, Bakery, Vegetables...)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Fixes plural display in admin


#  GenericProduct is the base product users compare (e.g. "Whole milk 1L", "Butter 250 g")
class GenericProduct(models.Model):
    UNIT_CHOICES = [
        ("L", "Liters"),
        ("ml", "Milliliters"),
        ("g", "Grams"),
        ("kg", "Kilograms"),
        ("pcs", "Pieces"),
        ("ks", "Ks (Czech for 'pieces')"),
    ]

    name = models.CharField(max_length=100)  # Generic name like "Whole milk"
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # e.g., 1.00
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)  # Unit dropdown in admin
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} – {self.amount} {self.unit}"


# Supermarket represents where the product is sold (e.g. Billa, Tesco, Albert)
class Supermarket(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ProductVariant is the real-world version of a generic product
# e.g., "Olma Selské mléko plnotučné 3,9%" from Tesco for 18.90 Kč
class ProductVariant(models.Model):
    generic_product = models.ForeignKey(GenericProduct, on_delete=models.CASCADE, related_name='variants')
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Specific brand/product name
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price in CZK
    last_updated = models.DateTimeField(auto_now=True)  # Auto-updates on save
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Optional product photo

    def __str__(self):
        return f"{self.name} at {self.supermarket.name} – {self.price} Kč"