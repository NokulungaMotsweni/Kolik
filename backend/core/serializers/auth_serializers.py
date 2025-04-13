import re
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


"""
RegisterSerializer for Kolik 

Handles:
- Email, phone, password collection
- Password confirmation
- Password strength validation (capital, number, symbol, etc.)
- Timestamps for T&C consent
- User marked inactive until phone/email verification is complete
"""
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        """
        Enforces password security using both Django validators and
        custom complexity rules (uppercase, lowercase, number, special char).
        """
        # Step 1: Run Django's built-in validators (e.g., min length, common password)
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        # Step 2: Custom rules
        if len(value) < 10:
            raise serializers.ValidationError("Password must be at least 10 characters long.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must include at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must include at least one special character.")

        return value

    def validate(self, data):
        """
        Validates that password and confirm_password fields match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Creates a new user. The account is inactive by default and awaits
        phone and email verification. Consent timestamps are stored.
        """
        validated_data.pop('confirm_password')  

        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
        user.is_active = False
        user.is_email_verified = False
        user.is_phone_verified = False
        user.terms_accepted_at = timezone.now()
        user.privacy_policy_accepted_at = timezone.now()
        user.save()

        return user