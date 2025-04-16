from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect





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
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response({
                "message": "Login successful.",
                "user_id": str(user.id),
                "email": user.email
            })
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