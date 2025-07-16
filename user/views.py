from django.contrib.auth import login, logout
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, LoginUserSerializer, ProfileUpdateSerializer, \
    PasswordChangeOTPGenerationSerializer, PasswordChangeOTPSerializer
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

        try:
            Token.objects.filter(user=user).delete()
            logout(request)

            return Response({
                "event": "logout_successful",
                "message": "User logged out and token deleted."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "event": "logout_failed",
                "message": f"Exception raised {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        try:
            serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response({
                    "event": "profile_update_successful",
                    "message": "User updated the profile successfully."
                }, status=status.HTTP_200_OK)

            return Response({
                "event": "profile_update_failed",
                "message": f"Validation error: {serializer.errors}"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "event": "profile_update_failed",
                "message": f"Exception raised: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PassChangeOTPGenerationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeOTPGenerationSerializer(data = request.data, context={"request" : request})

        try:
            if serializer.is_valid():
                serializer.create(request.data)
                return Response({
                    "event": "otp_generated_successfully",
                    "message": "OTP has been generated. Proceed to verify OTP.",
                    "user_id": request.user.id
                }, status=status.HTTP_201_CREATED)

            return Response({
                "event": "otp_invalid",
                "message": f"OTP invalid. Serializer errors: {serializer.errors}",
                "user_id": request.user.id
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "event": "otp_generation_failed",
                "message": f"Exception raised: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PasswordChangeOTPVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeOTPSerializer(data = request.data, context={"request" : request})

        try:
            if serializer.is_valid():
                return Response({
                    "event" : "otp_verified_successfully",
                    "message" : "OTP is valid and verified. Proceed to change password.",
                    "user_id" : request.user
                }, status = status.HTTP_200_OK)

            return Response({
                "event" : "otp_invalid",
                "message" : f"OTP invalid. Serializer errors: {serializer.errors}",
                "user_id" : request.user
            }, status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "event": "otp_verification_failed",
                "message": f"Exception raised: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


