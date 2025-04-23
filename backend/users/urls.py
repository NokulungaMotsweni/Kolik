"""
URL patterns for the 'users' app.

These endpoints handle:
- User registration
- Email existence check (step 1 of login)
- Password authentication (step 2 of login)
"""

from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, VerifyUserView, MFASetupView, VerifyMFAView, MFALoginView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', VerifyUserView.as_view(), name='verify-user'),
    path('mfa/setup/', MFASetupView.as_view(), name='mfa-setup'),
    path('verify-mfa/', VerifyMFAView.as_view(), name='verify-mfa'),
    path('mfa-login/', MFALoginView.as_view(), name='mfa-login'),
]