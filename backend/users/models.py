from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
import uuid
import hashlib
from django.contrib.auth import get_user_model
from .enums import AuditStatus, AuditAction


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    # hashed_password = models.CharField(max_length=255)

    # Optional (future): blocked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

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
    verification_type = models.ForeignKey('VerificationType', on_delete=models.CASCADE)
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

# Model to Represent the Verification Method Type, Whether it Requires a Token and the Duration of the Token
class VerificationType(models.Model):
    """
    Represents the Verification Method Type.

    Fields:
    - verification_type_id (AutoField): Primary key.
    - name (str): Type label (e.g., "Email", "Phone").
    - requires_token (boolean): Whether the Type Uses Token-Based Verification.
    - expires_on (timedelta): Token Validity Duration.
    """
    objects: models.Manager['UserVerification'] = models.Manager()  # Explicitly to Makes PyCharm Happy
    verification_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    requires_token = models.BooleanField(default=True)
    expires_on = models.DurationField()

    def __str__(self):
        return self.name

class LoginAttempts(models.Model):
    """
    Logs Each Login Attempt.

    Fields:
    - email_entered: What The User Typed As Their Email
    - success: Whether The Login was Successful
    - failure_reason: If Applicable, Description of Why it Failed
    - ip_address: IP Address of Login Attempt.
    - device: Optional Info: User-Agent or Device Name
    - timestamp: Auto-Filled with The Current Time
    """
    objects = models.Manager() # Explicitly defined for PyCharm code completion
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    email_entered = models.CharField(max_length=50)
    success = models.BooleanField()
    failure_reason = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    device = models.TextField(max_length=45, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_entered} - {'Success' if self.success else 'Failed'} at {self.timestamp}"

class AuditLog(models.Model):
    objects = models.Manager()
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100, choices=AuditAction.choices) # e.g login_attempt, email_verified
    path = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AuditStatus.choices) # SUCCESS / FAILED
    device = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.status} at {self.timestamp}"