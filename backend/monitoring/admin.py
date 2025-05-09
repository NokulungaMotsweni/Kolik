from django.contrib import admin
from .models import GeoAccessLog

class GeoAccessLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for viewing and managing GeoAccessLog entries.
    """
    list_display = ("timestamp", "ip_address", "country", "is_proxy", "status", "path")
    list_filter = ("status", "country", "is_proxy")
    search_fields = ("ip_address", "path")

admin.site.register(GeoAccessLog, GeoAccessLogAdmin)

# Register your models here.
