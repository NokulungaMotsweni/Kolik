import re
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from datetime import timedelta
from users.security import SecurityPolicy
User = get_user_model()
from users.models import UserVerification, VerificationType, LoginAttempts



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
        fields = ['name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        """
        Enforces password security using both Django validators and
        custom complexity rules (uppercase, lowercase, number, special char).
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        # Custom password validation rules
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
        email verification. Consent timestamps are stored.
        """
        validated_data.pop('confirm_password')

        # Create Inactive User Awaiting Email Verification
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],  # Store name here
        )
        user.is_active = False  # Only True after email verification
        user.is_email_verified = False
        user.terms_accepted_at = timezone.now()
        user.privacy_policy_accepted_at = timezone.now()
        user.save()

        # Lookup or Create the VerificationType (Email for now)
        verification_type, _ = VerificationType.objects.get_or_create(
            name='Email',
            defaults={
                'requires_token': True,
                'expires_on': timedelta(minutes=20)
            }
        )

        # Create UserVerification With Dynamic Expiry
        verification = UserVerification.objects.create(
            user=user,
            verification_type=verification_type,
            expires_at=timezone.now() + verification_type.expires_on
        )

        # Call generate_token Function
        raw_token = verification.generate_token()
        verification.save()

        # TEMPORARY FOR DEV/TESTING (REMOVE BEFORE PROD)
        print("Verification Token: ", raw_token)

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

        # Get IP and device (optional, improve later)
        ip = self.context['request'].META.get('REMOTE_ADDR')
        device = self.context['request'].META.get('HTTP_USER_AGENT', 'Unknown')

        #  Missing credentials
        if not email or not password:
            LoginAttempts.objects.create(
                email_entered=email or "",
                success=False,
                failure_reason="Missing Email or Password",
                ip_address=ip,
                device=device
            )
            raise serializers.ValidationError("Email and Password are Required.")

        # Find user if exists
        user_lookup = User.objects.filter(email=email).first()

        # Check if IP Blocked
        if not SecurityPolicy.handle_ip(ip, success=False):
            raise serializers.ValidationError("Too many failed login attempts. Try again later.")

        # Check User block Pre-Authentication
        if user_lookup:
            if user_lookup.is_blocked:
                if not user_lookup.cooldown_until:
                    raise serializers.ValidationError("Please Contact Support.")
                elif user_lookup.cooldown_until and user_lookup.cooldown_until > timezone.now():
                    raise serializers.ValidationError("Too many failed login attempts. Try again later.")

        # Log the login attempt BEFORE authentication
        LoginAttempts.objects.create(
            user=user_lookup if user_lookup else None,
            email_entered=email,
            success=False,
            failure_reason="Pending authentication.",
            ip_address=ip,
            device=device

        )

        # Authenticate user using Django's auth system
        user = authenticate(username=email, password=password)

        # Invalid Credentials
        if not user:
            LoginAttempts.objects.create(
                email_entered=email,
                success=False,
                failure_reason="Invalid Credentials",
                ip_address=ip,
                device=device
            )
            if user_lookup:
                SecurityPolicy.handle_user_login_attempts(
                    user=user_lookup,
                    success=False
            )
            raise serializers.ValidationError("Invalid Credentials.")

        # Account Inactive
        if not user.is_active:
            LoginAttempts.objects.create(
                email_entered=email,
                success=False,
                failure_reason="Account Inactive or Not Verified",
                ip_address=ip,
                device=device
            )
            SecurityPolicy.handle_user_login_attempts(
                user=user,
                success=False
            )
            raise serializers.ValidationError("Account is Inactive or Not Verified.")

        # Successful Login
        LoginAttempts.objects.create(
            email_entered=email,
            success=True,
            ip_address=ip,
            device=device
        )
        SecurityPolicy.handle_ip(ip, success=True)

        SecurityPolicy.handle_user_login_attempts(
            user=user,
            success=True,
        )

        # Attach the user to validated data for use in the view
        data["user"] = user
        return data


       