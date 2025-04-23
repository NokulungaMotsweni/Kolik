# Standard library imports
import hashlib
import base64
from io import BytesIO
from datetime import timedelta

# Django core imports
from django.utils import timezone
from django.contrib.auth import logout, login, get_user_model
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password

# Django REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Third-party packages
import pyotp
import qrcode

# Project-level imports
from utils.audit import log_login, log_action, get_login_failure_reason
from .serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser, UserVerification, VerificationType


User = get_user_model()



class RegisterView(APIView):
    """
    Handles secure user registration.
    Ensures full control for later features like OTP, reCAPTCHA, etc.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Account created. Please verify your email and phone number.",
                "user_id": str(user.id)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class LoginView(APIView):
    """
    Authenticates a user using email and password.
    Enforces MFA setup if not enabled. If MFA is enabled, waits for MFA code.
    """

    def post(self, request):
        email = request.data.get('email')  # Used for logging even on failure
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            #  MFA is not set up yet → force setup
            if not user.mfa_secret or not user.mfa_enabled:
                log_login(request, email=email, success=False, failure_reason="MFA setup required")
                return Response({
                    "mfa_setup_required": True,
                    "message": "MFA setup is required. Scan QR and verify your 6-digit code.",
                    "user_id": str(user.id),
                    "email": user.email
                }, status=status.HTTP_403_FORBIDDEN)

            #  MFA is enabled → go to second step (mfa-login)
            log_login(request, email=email, success=True, user=user)
            return Response({
                "mfa_required": True,
                "user_id": str(user.id),
                "email": user.email
            }, status=status.HTTP_200_OK)

        #  Login failed → log and return error
        failure_reason = get_login_failure_reason(serializer.errors)
        log_login(request, email=email, success=False, failure_reason=failure_reason)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    """
    Logs out the authenticated user by ending their session securely.
    - Requires POST request.
    - Requires user to be logged in.
    - Enforces CSRF protection.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Adding the Log for Successful LogOut
        log_action(request, action="logout", status="SUCCESS", user=user)
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

class VerifyUserView(APIView):
    """
    Verifies the User via Token, Token Must be Valid and Not Expired.
    The Verification Flags are Updated and User is Activated.
    """
    def post(self, request):
        token = request.data.get('token')
        if not token:
            log_action(request, action="email_verification", status="FAILED")
            return Response({"message": "Token is required."}, status=400)

        token_hash = hashlib.sha256(token.encode()).hexdigest()

        try:
            verification = UserVerification.objects.get(token_hash=token_hash, is_latest = True)
        except UserVerification.DoesNotExist:
            log_action(request, action="email_verification", status="FAILED")
            return Response({"message": "Token is Invalid or Expired."}, status=400)

        if verification.is_verified:
            log_action(request, action="email_verification", status="FAILED")
            return Response({"message": "Already Verified"}, status=200)

        if verification.expires_at < timezone.now():
            return Response({"message": "Token is Expired."}, status=400)

        verification.is_verified = True
        verification.verified_at = timezone.now()
        verification.save()

        # Update User Flags
        user = verification.user
        user.is_email_verified = True
        user.is_active = user.is_email_verified and user.is_phone_verified
        user.save()

        # Log Successful Verification
        log_action(request, action="email_verification", status="SUCCESS", user=user)
        return Response({"message": "Verification successful!"})







class MFASetupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Generate secret if not set
        if not user.mfa_secret:
            user.mfa_secret = pyotp.random_base32()
            user.save()

        # Create provisioning URL
        totp = pyotp.TOTP(user.mfa_secret)
        provisioning_url = totp.provisioning_uri(name=user.email, issuer_name="Kolik")

        # Generate QR code
        qr = qrcode.make(provisioning_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_image_b64 = base64.b64encode(buffer.getvalue()).decode()

        # setup start is logged
        log_action(request, action="mfa_setup_started", status="SUCCESS", user=user)

        return Response({
            "secret": user.mfa_secret,
            "qr_code_base64": qr_image_b64
        }, status=status.HTTP_200_OK)






class VerifyMFAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        user = request.user

        if not user.mfa_secret:
            log_action(request, action="mfa_verified", status="FAILED", user=user)
            return Response({"error": "MFA is not set up."}, status=400)

        if not code:
            log_action(request, action="mfa_verified", status="FAILED", user=user)
            return Response({"error": "Code is required."}, status=400)

        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            user.mfa_enabled = True
            user.save()
            log_action(request, action="mfa_verified", status="SUCCESS", user=user)
            return Response({"message": "MFA verification successful!"}, status=200)
        else:
            log_action(request, action="mfa_verified", status="FAILED", user=user)
            return Response({"error": "Invalid code. Try again."}, status=400)




class MFALoginView(APIView):
    """
    Verifies the 6-digit MFA code during login.
    Accepts email and MFA code. If valid, logs the user in.
    """

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            log_action(request, action="mfa_login", status="FAILED")
            return Response({"error": "Email and MFA code are required."}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            log_action(request, action="mfa_login", status="FAILED")
            return Response({"error": "User not found."}, status=404)

        if not user.mfa_enabled or not user.mfa_secret:
            log_action(request, action="mfa_login", status="FAILED", user=user)
            return Response({"error": "MFA is not enabled for this account."}, status=400)

        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            login(request, user)
            log_action(request, action="mfa_login", status="SUCCESS", user=user)
            log_login(request, email=email, success=True, user=user)  # Record login success
            return Response({
                "message": "MFA verification successful. You are now logged in.",
                "user_id": str(user.id),
                "email": user.email
            }, status=200)
        else:
            log_action(request, action="mfa_login", status="FAILED", user=user)
            log_login(request, email=email, success=False, user=user, failure_reason="Invalid MFA code")
            return Response({"error": "Invalid MFA code."}, status=400)








class PasswordResetRequestView(APIView):
    """
    Step 1: Accept user's email and generate a password reset token.
    """

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal if user exists
            return Response({"message": "If this email exists, a reset link will be sent."}, status=200)

        # Get or create password reset verification type
        verification_type, _ = VerificationType.objects.get_or_create(
            name="Password Reset",
            defaults={"requires_token": True, "expires_on": timedelta(minutes=30)}
        )

        # Invalidate previous tokens
        UserVerification.objects.filter(
            user=user,
            verification_type=verification_type,
            is_latest=True
        ).update(is_latest=False)

        # Create new token
        verification = UserVerification.objects.create(
            user=user,
            verification_type=verification_type,
            expires_at=timezone.now() + verification_type.expires_on,
            is_latest=True
        )

        raw_token = verification.generate_token()
        verification.save()

        # TEMP: print raw token (we will email this later)
        print("RESET TOKEN:", raw_token)

        return Response({"message": "If this email exists, a reset link will be sent."}, status=200)   





class PasswordResetConfirmView(APIView):
    """
    Step 2: Confirm token and allow the user to set a new password.
    """

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not token or not new_password or not confirm_password:
            return Response({"error": "Token, new_password, and confirm_password are required."}, status=400)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=400)

        # Validate token
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        try:
            verification = UserVerification.objects.get(token_hash=token_hash, is_latest=True)
        except UserVerification.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=400)

        if verification.expires_at < timezone.now():
            return Response({"error": "Token expired."}, status=400)

        # Update password
        user = verification.user
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as e:
            return Response({"error": e.messages}, status=400)

        user.set_password(new_password)
        user.save()

        # Mark verification as used
        verification.is_verified = True
        verification.verified_at = timezone.now()
        verification.save()

        return Response({"message": "Password has been reset successfully."}, status=200)                 