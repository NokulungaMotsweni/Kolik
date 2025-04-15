from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'is_phone_verified')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'is_phone_verified')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Verification'), {'fields': ('is_email_verified', 'is_phone_verified')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Consents'), {'fields': ('terms_accepted_at', 'privacy_policy_accepted_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
