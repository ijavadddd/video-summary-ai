from django.urls import path
from accounts.views import (
    LoginView,
    SignUpView,
    LogoutView,
    RecoveryPasswordView,
    VerifyOTPView,
)


app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "recovery-password/", RecoveryPasswordView.as_view(), name="recovery_password"
    ),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
]
