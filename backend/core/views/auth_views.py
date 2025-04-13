from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers.auth_serializers import RegisterSerializer
from core.models.users import CustomUser
from core.serializers.auth_serializers import LoginSerializer






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




class CheckEmailView(APIView):
    """
    Step 1: Validates if a user exists with the given email and is active.
    """
    def post(self, request):
        email = request.data.get("email", "").strip().lower()

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)

            if not user.is_active:
                return Response({"error": "Account is inactive or unverified."}, status=403)

            return Response({
                "message": "Email is valid. Continue to password entry.",
                "user_id": str(user.id)
            })

        except CustomUser.DoesNotExist:
            return Response({"error": "No account found with this email."}, status=404)



class LoginView(APIView):
    """
    Step 2: Authenticates a user using email and password.
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
        return Response(serializer.errors, status=400)                    