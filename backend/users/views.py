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
    Logs success and failure attempts.
    """

    def post(self, request):
        email = request.data.get('email') # Used for Logging Even if it is Fails
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Log Successful Login
            log_login(request, email=email, success=True, user=user)

            return Response({
                "message": "Login successful.",
                "user_id": str(user.id),
                "email": user.email
            })

        # Log Failed Login Attempt
        log_login(request, email=email, success=False, failure_reason=str(serializer.errors))

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

        return Response({"message": "Verification successful!"})