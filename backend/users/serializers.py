import re
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from users.models import UserVerification
from datetime import timedelta
User = get_user_model()



"""
RegisterSerializer for Kolik 

Handles:
- Email, phone, password collection
- Password confirmation
- Password strength validation (capital, number, symbol, etc.)
- Timestamps for T&C consent
- User marked inactive until phone/email verification is complete
- User Verification
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

        # Creation of Verification Token
        verification = UserVerification.objects.create(
            user=user,
            # Expires after 20 minutes
            expires_at=timezone.now() + timedelta(minutes=20)
        )
        # Call generate_token Function
        raw_token = verification.generate_token()
        verification.save()

        # THIS IS TEMPORARY IF WE DECIDE TO KEEP THE TOKEN AND FIGURE OUT HOW TO EMAIL
        print("Verification Token: ", raw_token) # RAW TOKEN AS IT WILL GO TO THE USER
        return user







class LoginSerializer(serializers.Serializer):
    """
    Handles user login by validating email and password credentials.

    - Verifies that both fields are provided
    - Authenticates user using Django's built-in `authenticate`
    - Checks if the user account is active (i.e., not disabled or pending verification)
    - If successful it attaches the authenticated user to the validated data
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Ensure both fields are provided
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate user using Django's auth system
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        # Ensure the account is active (not disabled or pending verification)
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive or not verified.")

        # Attach the user to validated data for use in the view
        data["user"] = user
        return data


# TODO 
# - Add rate limiting 
# - Log login attempts 
# - Support session tokens
# - Detect and block suspicious login behavior (e.g., too many logins from new IPs)
# - Integrate 2FA 
# - Add account lockout after multiple failed attempts (with cooldown)
# - Optionally notify users on successful login from a new device or location        