from django.db import models
from django.conf import settings

class Monitoring(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=3, null=True, blank=True)
    is_proxy = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    path = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='geo_access_attempts'
    )

    def __str__(self):
        if self.user:
            # Try email, fallback to ID
            user_info = self.user.email if hasattr(self.user, 'email') else f"User ID {self.user.id}"
        else:
            user_info = "Anonymous"

        status = "Blocked" if self.blocked else "Allowed"
        return f"{self.timestamp} — {user_info} — {self.ip_address} — {self.country or 'Unknown'} — {status}"
# Create your models here.
