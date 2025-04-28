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
from .models import CustomUser, UserVerification, LoginAttempts, AuditLog, IPAddressBan


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin to support:
    - Email-based login
    - MFA status
    - Custom field organization in the admin panel
    """
    model = CustomUser

    # Columns visible in the admin user list
    list_display = (
        'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'mfa_enabled'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'mfa_enabled')
    ordering = ('email',)
    search_fields = ('email', 'name')

    # Fields shown when viewing a user object
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (_('Verification'), {'fields': ('is_email_verified', 'mfa_enabled')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Consents'), {'fields': ('terms_accepted_at', 'privacy_policy_accepted_at')}),
    )

    # Fields shown when adding a new user from the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
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

@admin.register(LoginAttempts)
class LoginAttemptsAdmin(admin.ModelAdmin):
    """
    Admin Configuration for the LoginAttempts Model.
    Provides Visibility into All the Login Attempts For Audit/Security Review.
    """
    list_display = (
        'timestamp', 'email_entered', 'success', 'failure_reason',
        'user', 'ip_address', 'device'
    )
    list_filter = ('success', 'timestamp')
    search_fields = ('email_entered', 'failure_reason', 'ip_address', 'user__email')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for AuditLog model.
    Tracks all user actions and system events.
    """
    list_display = (
        'timestamp', 'action', 'status', 'user', 'path', 'device'
    )
    list_filter = ('action', 'status', 'timestamp')
    search_fields = ('user__email', 'action', 'path', 'device')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
