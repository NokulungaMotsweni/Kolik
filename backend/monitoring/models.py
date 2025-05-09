from django.db import models
from django.conf import settings

class GeoAccessLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=3, null=True, blank=True)
    is_proxy = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    path = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.timestamp} | {self.ip_address} | {self.status}"
# Create your models here.
