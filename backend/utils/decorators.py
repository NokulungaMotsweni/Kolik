from functools import wraps
from users.models import AuditLog
from users.enums import AuditAction, AuditStatus
from utils.request import get_client_ip

def log_email_action(audit_action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request") or (args[0] if args else None)
            user = kwargs.get("user") or getattr(request, "user", None)

            ip_address = get_client_ip(request) if request else None
            device = request.META.get("HTTP_USER_AGENT") if request else None
            path = request.path if request else "N/A"

            try:
                result = func(*args, **kwargs)

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
                AuditLog.objects.create(
                    user=user,
                    action=audit_action,
                    path=path,
                    ip_address=ip_address,
                    device=device,
                    status=AuditStatus.FAILED
                )
                raise
        return wrapper
    return decorator
