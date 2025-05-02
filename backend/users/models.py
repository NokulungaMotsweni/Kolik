from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from config import settings
from .managers import CustomUserManager
import uuid
import hashlib
from django.contrib.auth import get_user_model
from .enums import AuditStatus, AuditAction, CookieType, CookieConsentType, SignupFailureReason


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    # hashed_password = models.CharField(max_length=255)

    # Optional (future): blocked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    # Verification flags
    is_email_verified = models.BooleanField(default=False)

    # Consent timestamps
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    privacy_policy_accepted_at = models.DateTimeField(null=True, blank=True)

    #MFA
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)

    # Required fields
    is_active = models.BooleanField(default=False)  # Only True after both verifications
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Field For Rate Limiting
    login_attempt_count = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    cooldown_until = models.DateTimeField(null=True, blank=True)
    cooldown_strikes = models.IntegerField(default=0) # Number of Cooldowns

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

    # User associated with attempt (if identifiable); Nullable
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    # Email address entered during login attempt
    email_entered = models.CharField(max_length=50)

    # If the login is successful or not
    success = models.BooleanField()

    # Login failure reason, if applicable
    failure_reason = models.TextField(null=True, blank=True)

    # IP address from which login was attempted
    ip_address = models.GenericIPAddressField()

    # Optional device info
    device = models.TextField(max_length=45, null=True, blank=True)

    # Auto capture of the timestamp when login was attempted
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_entered} - {'Success' if self.success else 'Failed'} at {self.timestamp}"

    class Meta:
        # Index to speed up queries in the common lookup fields
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["email_entered"]),
        ]

class SignUpAttempts(models.Model):
    """
    Logs each user signup attempt.
    Includes:
    - Whether it was successful or not.
    - IP Address of signup attempt.
    - Other relevant metadata.
    """
    objects = models.Manager()
    email_entered = models.CharField(max_length=50) # Email address used for sign up

    # Indicated whether the signup was successful
    success = models.BooleanField()

    # Failure Reason if Applicable
    failure_reason = models.CharField(
        max_length=50,
        choices=SignupFailureReason.choices,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField() # Signin attempt IP Address
    device = models.TextField(max_length=45, null=True, blank=True) # Device/User agent info, optional
    timestamp = models.DateTimeField(auto_now_add=True) # When the signup attempt occurred

    def __str__(self):
        return f"{self.email_entered} - {'Success' if self.success else 'Failed'} at {self.timestamp}"

    class Meta:
        # Add indexes to improve query performance for common lookup fields
        indexes = [
            models.Index(fields=["email_entered"]),
            models.Index(fields=["ip_address"]),
        ]


class AuditLog(models.Model):
    """
    Stores Secure Audit Logs.
    Tracks Login Attempts and Email Verification (for now).
    """
    objects = models.Manager()
    log_id = models.AutoField(primary_key=True)
    # User that is associated with the action (nullable should the user be unknown)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100, choices=AuditAction.choices) # e.g login_attempt, email_verified
    path = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AuditStatus.choices) # SUCCESS / FAILED
    device = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String Representation of AuditLog entry.
        Returns:
            - Action
            - Status
            - Timestamp
        """
        return f"{self.action} - {self.status} at {self.timestamp}"

class Cookies(models.Model):
    """
    Stores the individual cookies associated with each user.
    Includes:
        - Cookie's Purpose
        - Cookie's Expiration
        - Security Settings
        - Name: Type of Cookie
    """

    # Link to the user; nullable if the user gets deleted
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    # Cookie name (e.g., csrftoken, sessionID)
    cookie_name = models.CharField(max_length=40)

    # Cookie Value (session token / tracking ID etc.)
    cookie_value = models.TextField()

    # Cookie type using predefined set of choices
    cookie_type = models.CharField(max_length=20, choices=CookieType.choices)

    # Domain scope for which the cookie is valid.
    domain = models.CharField(max_length=255, null=True, blank=True)

    # Path scope for which the cookie is valid
    path = models.CharField(max_length=255, null=True, blank=True)

    # Cookie expiration datetime
    expires = models.DateTimeField(blank=True, null=True)

    # If Truem cookie is only sent obly over HTTPS
    secure = models.BooleanField(default=False)

    # If True, cookie is inaccessible to client-side scripts
    http_only = models.BooleanField(default=False)

    # Creation date of the cookie record
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String Representation of Cookies entry.
        Returns:
            - USer's email / Username / Falls back to user ID
        """
        identifier = getattr(self.user, 'email', None) or getattr(self.user, 'username', None) or f"User {self.user.id}"
        return f"{self.cookie_name} ({self.cookie_type}) for {identifier}"

class CookieConsent(models.Model):
    """
    Records user's cookie consent decision.
    Stores:
        - Consent
        - Policy Version
        - Date when it happened
    """
    # One-to-one link with the user; each user has exactly one CookieConsent record
    objects = models.Manager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    # Whether consent has been given for cookie usage
    consent_given = models.BooleanField(default=False)

    # Version of the cookie policy the user agreed to
    policy_version = models.CharField(max_length=10)

    # Selection of Cookies
    cookie_selection = models.CharField(
        max_length=30,
        choices=CookieConsentType.choices,
        default=CookieConsentType.MANDATORY_ONLY
    )

    # timestamp when the consent decision was recorded
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Representation of CookieConsent entry.
        Shows:
            - Consent: True/False
            - User's email address
            - Policy Version
        """
        return f"Consent {self.consent_given} for {self.user.email} (v{self.policy_version})"


class IPAddressBan(models.Model):
    """
    Tracks IP Addresses that are temporarily/permanently banned due to excessive failed login attempts.
    """
    objects = models.Manager()

    # Tracked IP Address, Unique
    ip_address = models.GenericIPAddressField(unique=True)

    # Number of failed login attempts
    login_attempt_count = models.IntegerField(default=0)

    # Number of failed signup attempts
    signup_attempt_count = models.IntegerField(default=0)

    # Optional timestamp until which IP is blocked; Null: No temporary block
    blocked_until = models.DateTimeField(null=True, blank=True)

    # If IP Address is permanently/temporarily blocked
    is_blocked = models.BooleanField(default=False)

    # Timestamp of the last login attempt from this IP Address
    last_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
                Returns:
                     Readable string representation of the IP address status.
                """
        return f"IP {self.ip_address} - {'Blocked' if self.is_blocked else 'Active'}"