from functools import wraps
from users.models import AuditLog
from users.enums import AuditAction, AuditStatus
from utils.request import get_client_ip

def log_email_action(audit_action):
    """
        Decorator to log audit events for email-related actions.

        Logs success or failure of the decorated function call
        with metadata such as IP address, user agent, and request path.

        Args:
            audit_action (AuditAction): Enum value specifying the type of email action being audited.

        Returns:
            function: Wrapped function with audit logging applied.
        """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to extract request and user from kwargs or args
            request = kwargs.get("request") or (args[0] if args else None)
            user = kwargs.get("user") or getattr(request, "user", None)

            # Extract IP, user-agent, and path for audit logging
            ip_address = get_client_ip(request) if request else None
            device = request.META.get("HTTP_USER_AGENT") if request else None
            path = request.path if request else "N/A"

            try:
                # Execute the decorated function
                result = func(*args, **kwargs)

                # Log successful audit entry
                AuditLog.objects.create(
                    user=user,
                    action=audit_action,
                    path=path,
                    ip_address=ip_address,
                    device=device,
                    status=AuditStatus.SUCCESS
                )
                return result

            except Exception as e:
                # Log failed audit entry
                AuditLog.objects.create(
                    user=user,
                    action=audit_action,
                    path=path,
                    ip_address=ip_address,
                    device=device,
                    status=AuditStatus.FAILED
                )
                raise # Re-raise exception after logging
        return wrapper
    return decorator
