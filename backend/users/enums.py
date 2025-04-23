from django.db import models

class AuditAction(models.TextChoices):
    LOGIN_ATTEMPT = "login_attempt", "Login Attempt"
    PASSWORD_RESET = "password_reset", "Password Reset"
    EMAIL_VERIFIED = "email_verified", "Email Verified"
    LOGOUT = "logout", "Logout"
    PROFILE_UPDATED = "profile_updated", "Profile Updated"
    MFA_SETUP_STARTED = "mfa_setup_started", "MFA Setup Started"
    MFA_VERIFIED = "mfa_verified", "MFA Verified"
    MFA_LOGIN = "mfa_login", "MFA Login"

class AuditStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"

class LoginFailureReason:
    INVALID_CREDENTIALS = "invalid_credentials"
    MISSING_EMAIL = "missing_email"
    MISSING_PASSWORD = "missing_password"
    INACTIVE_ACCOUNT = "inactive_account"
    UNKNOWN = "unknown"
