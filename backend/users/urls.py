"""
URL patterns for the 'users' app.

These endpoints handle:
- User registration
- Email existence check (step 1 of login)
- Password authentication (step 2 of login)
"""

from django.urls import path
from users.views import RegisterView, LoginView, CheckEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
]