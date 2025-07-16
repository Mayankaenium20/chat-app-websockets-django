from django.urls import path

from .views import SignUpView, LoginView, LogoutView, UpdateUserProfileView
from .views import PassChangeOTPGenerationView, PasswordChangeOTPVerificationView

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name = "user-signup"),
    path("login/", LoginView.as_view(), name = "user-login"),
    path("logout/", LogoutView.as_view(), name = "user-logout"),
    path("profile-update/", UpdateUserProfileView.as_view(), name = "profile-update"),

    # otp generation
    path('otp-generation/', PassChangeOTPGenerationView.as_view(), name = "otp-gen"),
    path('otp-verification/', PasswordChangeOTPVerificationView.as_view(), name = "otp-ver"),
]