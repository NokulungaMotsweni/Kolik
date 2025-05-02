from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.serializers import RegisterSerializer

class TestRegisterSerializer(TestCase):
    def test_weak_password_is_rejected(self):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/", {}, HTTP_USER_AGENT="TestAgent", REMOTE_ADDR="127.0.0.1")

        serializer = RegisterSerializer(
            data={
                "name": "Test User",
                "email": "test@example.com",
                "password": "weak",
                "confirm_password": "weak"
            },
            context={"request": request}
        )

        print("\nIS VALID:", serializer.is_valid())
        print("ERRORS:", serializer.errors)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_strong_password_is_accepted(self):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/", {}, HTTP_USER_AGENT="TestAgent", REMOTE_ADDR="127.0.0.1")

        serializer = RegisterSerializer(
            data={
                "name": "Secure User",
                "email": "valid@example.com",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!"
            },
            context={"request": request}
        )

        print("\nIS VALID:", serializer.is_valid())
        print("VALIDATED:", serializer.validated_data)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("password", serializer.errors)

# Create your tests here.
