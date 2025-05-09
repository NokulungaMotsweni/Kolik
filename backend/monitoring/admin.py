from django.contrib import admin
from .models import GeoAccessLog

class GeoAccessAttemptAdmin(admin.ModelAdmin):
    llist_display = ("timestamp", "ip_address", "country", "is_proxy", "status", "path")
    list_filter = ("status", "country", "is_proxy")
    search_fields = ("ip_address", "path")

# Register your models here.
