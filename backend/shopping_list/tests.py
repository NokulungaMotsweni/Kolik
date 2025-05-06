from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from products.models import GenericProduct, ProductVariant, Supermarket
from shopping_list.models import ShoppingList, ShoppingListItem


User = get_user_model()

class ShoppingCartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="password")
        self.client = APIClient()
        self.client.login(username="alice", password="password")

        self.supermarket = Supermarket.objects.create(name="Tesco")
        self.product = GenericProduct.objects.create(name="Milk")
        self.variant = ProductVariant.objects.create(
            name="Tesco Milk 1L",
            generic_product=self.product,
            supermarket=self.supermarket,
            price=1.25
        )

    def add_item_to_cart(self, locked=True):
        return self.client.post(reverse("add_to_cart"), {
            "product_id": self.product.id,
            "quantity": 2,
            "variant_id": self.variant.id,
            "locked": locked
        })


def test_add_to_cart(self):
    response = self.add_item_to_cart()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("product", response.data)


def test_view_cart(self):
    self.add_item_to_cart()
    response = self.client.get(reverse("view_cart"))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreater(len(response.data["cart"]), 0)


def test_compare_cart(self):
    self.add_item_to_cart()
    response = self.client.get(reverse("compare_user_cart"))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("supermarket_totals", response.data)


def test_mixed_basket(self):
    self.add_item_to_cart()
    response = self.client.get(reverse("mixed_basket"))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("items", response.data)


def test_supermarket_breakdown(self):
    self.add_item_to_cart()
    basket = [{"product_id": self.product.id, "quantity": 2}]
    response = self.client.post(reverse("supermarket_breakdown"), {
        "basket": basket,
        "supermarket": "Tesco"
    })
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("items", response.data)

# Create your tests here.
