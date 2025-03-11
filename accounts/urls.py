from django.urls import path
from accounts.views import (
    LoginView,
    SignUpView,
    LogoutView,
    RecoveryPasswordView,
    SetPasswordView,
)


app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "recovery-password/", RecoveryPasswordView.as_view(), name="recovery_password"
    ),
    path(
        "set-password/<uidb64>/<token>/", SetPasswordView.as_view(), name="set_password"
    ),
]
