from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
import uuid
import hashlib


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    # hashed_password = models.CharField(max_length=255)

    # Verification flags
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # Consent timestamps
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    privacy_policy_accepted_at = models.DateTimeField(null=True, blank=True)

    # Required fields
    is_active = models.BooleanField(default=False)  # Only True after both verifications
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Model to Manage User Verification token and Tracking Their Status
class UserVerification(models.Model):
    """
    Stores User Verification Data.
    This Data is Used to Verify the Identity of the User via Time-Limited Tokens.
    """
    verification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verifications"
    )
    token_hash = models.CharField(max_length=64)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempt_number = models.IntegerField(default=0)
    is_latest = models.BooleanField(default=True)
    objects: models.Manager['UserVerification'] = models.Manager()

    def generate_token(self):
        """
        Generates a New Unhashed Token and Stores the SHA256 Hash of the Token.

        Returns:
            str: The unhashed SHA256 Hash of the Token is Sent to The User.
        """
        raw_token = str(uuid.uuid4())
        self.token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        return raw_token

class VerificationType(models.Model):
    verification_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    requires_token = models.BooleanField(default=True)
    expires_on = models.DurationField()  # Matches INTERVAL from your schema

    def __str__(self):
        return self.name
