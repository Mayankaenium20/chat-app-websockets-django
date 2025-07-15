from django.urls import path

from .views import SignUpView, LoginView, LogoutView

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name = "user-signup"),
    path("login/", LoginView.as_view(), name = "user-login"),
    path("logout/", LogoutView.as_view(), name = "user-logout"),
]