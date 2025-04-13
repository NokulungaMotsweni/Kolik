from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers.auth_serializers import RegisterSerializer
from core.models.users import CustomUser

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