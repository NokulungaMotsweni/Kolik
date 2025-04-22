from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser, UserVerification
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import hashlib
from utils.audit import log_login, log_action, get_login_failure_reason
import pyotp
import qrcode
import base64
from io import BytesIO
from django.contrib.auth import login



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
            return Response({"error": "MFA is not set up."}, status=400)

        if not code:
            return Response({"error": "Code is required."}, status=400)

        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            user.mfa_enabled = True
            user.save()
            return Response({"message": "MFA verification successful!"}, status=200)
        else:
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
            return Response({"error": "Email and MFA code are required."}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if not user.mfa_enabled or not user.mfa_secret:
            return Response({"error": "MFA is not enabled for this account."}, status=400)

        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            login(request, user)
            return Response({
                "message": "MFA verification successful. You are now logged in.",
                "user_id": str(user.id),
                "email": user.email
            }, status=200)
        else:
            return Response({"error": "Invalid MFA code."}, status=400)            