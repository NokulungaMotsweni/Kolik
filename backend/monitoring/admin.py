from django.contrib import admin
from .models import GeoAccessLog

class GeoAccessAttemptAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "ip_address", "country", "is_proxy", "status", "path")
    list_filter = ("status", "country", "is_proxy")
    search_fields = ("ip_address", "path")

    admin.site.register(GeoAccessLog, GeoAccessAttemptAdmin)

# Register your models here.
