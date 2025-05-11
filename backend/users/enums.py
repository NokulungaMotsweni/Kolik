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
    SIGNUP_SUCCESSFUL = "signup_successful", "Signup Successful"
    EMAIL_VERIFICATION_SENT = "email_verification_sent", "Email Verification Sent"
    PASSWORD_RESET_SENT = "password_reset_sent", "Password Reset Sent"
    EMAIL_CHANGE_VERIFICATION_SENT = "email_change_verification_sent", "Email Change Verification Sent"
    PASSWORD_CHANGE_SUCCESS = "Password Change Success"
    EMAIL_CHANGE_SUCCESS = "Email Change Success"

    # For Security
    USER_TEMP_BLOCKED = "user_temp_blocked", "User Temporarily Blocked"
    USER_PERMANENTLY_BLOCKED = "user_permanently_blocked", "User Permanently Blocked"
    IP_BLOCKED = "ip_blocked", "IP Blocked"
    RATE_LIMIT_TRIGGERED = "rate_limit_triggered", "Rate Limit Triggered"

class AuditStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"

class LoginFailureReason:
    INVALID_CREDENTIALS = "invalid_credentials"
    MISSING_EMAIL = "missing_email"
    MISSING_PASSWORD = "missing_password"
    INACTIVE_ACCOUNT = "inactive_account"
    UNKNOWN = "unknown"

class CookieType(models.TextChoices):
    MANDATORY = 'mandatory', 'Mandatory'
    ANALYTICS = 'analytics', 'Analytics'

class CookieConsentType(models.TextChoices):
    MANDATORY_ONLY = 'mandatory_only', 'Mandatory Only'
    MANDATORY_AND_ANALYTICS = 'mandatory_and_analytics', 'Mandatory and Analytics'

class SignupFailureReason(models.TextChoices):
    EMAIL_ALREADY_EXISTS = "email_already_exists", "Email already exists"
    BLOCKED_IP = "blocked_ip", "IP address is blocked"
    RATE_LIMITED = "rate_limited", "Rate limited"
    PASSWORD_TOO_WEAK = "password_too_weak", "Password too weak"
    MISMATCHED_PASSWORDS = "mismatched_passwords", "Passwords do not match"
    UNKNOWN = "unknown", "Unknown error"
