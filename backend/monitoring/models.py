from django.db import models
from django.conf import settings

class GeoAccessLog(models.Model):
    """
    Stores metadata about access attempts based on geolocation.

    Fields:
    timestamp (datetime): Timestamp when this access was attempted.
    ip_address (str): IP address of this access attempt.
    country (str): Country code for this access attempt.
    is_proxy (bool): Whether this access attempt is proxied.
    status (str): Status of this access attempt.
    path (str): Path of this access attempt.
    """

    # Log Creation
    timestamp = models.DateTimeField(auto_now_add=True)

    # Client IP Address
    ip_address = models.GenericIPAddressField()

    # Country Code
    country = models.CharField(max_length=3, null=True, blank=True)

    # Whether IP is a proxy or VPN
    is_proxy = models.BooleanField(default=False)

    # Access Status Description
    status = models.CharField(max_length=50)

    # Accessed URL path
    path = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns a string representation of the access log entry.
        """
        return f"{self.timestamp} | {self.ip_address} | {self.status}"
# Create your models here.