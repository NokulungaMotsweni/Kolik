from users.models import AuditLog, LoginAttempts
from users.enums import  LoginFailureReason

def log_action(request, action, status, user=None):
    """
       Generic Logging Function to Record Any Action in AuditLog.
       """
    ip = request.META.get('REMOTE_ADDR', '')
    device = request.META.get('HTTP_USER_AGENT', 'Unknown')
    path = request.path

    AuditLog.objects.create(
        user=user or (request.user if request.user.is_authenticated else None),
        action=action,
        status=status,
        path=path,
        device=device,
        ip_address=ip
    )

def log_login(request, email, success, user=None, failure_reason=None):
    """
        Logs a Login Attempt to Both LoginAttempts and AuditLog.
        """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0].strip()
    device = request.META.get('HTTP_USER_AGENT', 'Unknown')
    path = request.path

    # Log the Login Attempt
    LoginAttempts.objects.create(
        user=user if success else None,
        email_entered=email,
        success=success,
        failure_reason=failure_reason,
        ip_address=ip,
        device=device
    )
    # Log a General Audit Entry
    log_action(
        request=request,
        action="login_attempt",
        status="SUCCESS" if success else "FAILED",
        user=user if success else None
    )


def get_login_failure_reason(errors):
    """
    Normalize Serializer Errors Into a Failure Reason Code.
    """
    if not errors:
        return LoginFailureReason.UNKNOWN

    if "non_field_errors" in errors:
        message = errors["non_field_errors"][0].lower()
        if "unable to log in" in message:
            return LoginFailureReason.INVALID_CREDENTIALS
        if "inactive" in message:
            return LoginFailureReason.INACTIVE_ACCOUNT

    if "email" in errors:
        return LoginFailureReason.MISSING_EMAIL

    if "password" in errors:
        return LoginFailureReason.MISSING_PASSWORD

    return LoginFailureReason.UNKNOWN

