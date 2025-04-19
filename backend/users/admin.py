"""
Admin configuration for the CustomUser model.

This custom admin panel:
- Displays additional fields like phone number and verification status
- Allows admin filtering and searching by email or phone
- Organizes fields into clear sections (verification, permissions, consents, etc.)
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserVerification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin to support:
    - Email-based login
    - Phone number field
    - Email and phone verification flags
    - Custom field organization in the admin panel
    """
    model = CustomUser

    # Columns visible in the admin user list
    list_display = (
        'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser',
        'is_email_verified', 'is_phone_verified'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'is_phone_verified')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')

    # Fields shown when viewing a user object
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Verification'), {'fields': ('is_email_verified', 'is_phone_verified')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Consents'), {'fields': ('terms_accepted_at', 'privacy_policy_accepted_at')}),
    )

    # Fields shown when adding a new user from the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserVerification Model.
    Tracks Token Generation, Token Expiry and Verification Status.
    """
    list_display = (
        'verification_id', 'token_hash', 'is_verified', 'attempt_number',
        'is_latest', 'created_at', 'expires_at', 'verified_at'
    )
    list_filter = ('is_verified', 'is_latest')
    search_fields = ('token_hash',)
    readonly_fields = ('created_at', 'verified_at')