from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, LoginUserSerializer
# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = Token.objects.create(user = user)
            return Response({
                "event" : "user_registered",
                "message" : "User saved successfully!",
                "username" : user.username,
                "email" : user.email,
                "token" : token.key
            },
            status = status.HTTP_201_CREATED)

        return Response({"event" : "user_registration_failed", "message" : f"User could not be created. Serializer error: {serializer.errors}"},
                        status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "event" : "login_successful",
                "message" : "User logged in successfully.",
                "username" : user.username,
                "token" : token.key
            },
            status = status.HTTP_200_OK)

        return Response({"event" : "login_unsuccessful", "message" : f"User log in unsuccessful."},
                        status = status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            logout(request)

            return Response({
                "event": "logout_successful",
                "message": "User logged out and token deleted."
            }, status=status.HTTP_200_OK)

        return Response({
            "event": "logout_failed",
            "message": "User is not authenticated."
        }, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserProfileView(RetrieveUpdateDestroyAPIView):
    pass
#IMP tomorrow
# refer: figma whatsapp