"""
Custom user manager for the Kolik app.

Overrides Django's default user creation logic to:
- Use email and phone number instead of username
- Provide custom methods for creating users and superusers
"""

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.

    Handles user creation using email + phone number (no username field),
    and ensures superusers have all required permissions.
    """

    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and phone number.

        Args:
            email (str): User's email (used as the login identifier)
            phone_number (str): User's phone number
            password (str): Raw password
            extra_fields (dict): Additional fields like is_active, is_verified, etc.

        Raises:
            ValueError: If email or phone number is missing

        Returns:
            CustomUser instance
        """
        if not email:
            raise ValueError("The Email must be set")
        if not phone_number:
            raise ValueError("The Phone number must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and returns a superuser (admin) with full permissions.

        Sets:
            - is_staff = True
            - is_superuser = True
            - is_active = True

        Raises:
            ValueError: If required superuser flags are missing
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, phone_number, password, **extra_fields)