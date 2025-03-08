from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from accounts.forms import LoginForm, SignUpForm
from django.contrib import messages
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.forms import RecoveryPasswordForm, VerifyOTPForm
from django.core.mail import send_mail
from accounts.utils import generate_otp
from django.http import JsonResponse


class LoginView(View):
    template_name = "accounts/login.html"
    login_form_class = LoginForm
    signup_form_class = SignUpForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next") or reverse_lazy("video_summary:main")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("video_summary:main")

        return super().dispatch(request, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "login_form": self.login_form_class(),
                "signup_form": self.signup_form_class(),
                "show_signup": False,  # Show login form by default
            },
        )

    def post(self, request, *args, **kwargs):
        login_form = self.login_form_class(request.POST)

        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password"]
            )
            if user:
                login(request, user)
                messages.success(
                    request,
                    f"خوش آمدی {user.username}",
                    "text-green-700 bg-green-300 border-green-400",
                )
                return redirect(self.next)
            messages.error(
                request,
                "نام کاربری یا رمزعبور صحیح نمی‌باشد",
                "text-red-700 bg-red-300 border-red-400",
            )
        return render(
            request,
            self.template_name,
            {
                "login_form": login_form,
                "signup_form": self.signup_form_class(),
                "show_signup": False,
            },
        )


class SignUpView(View):
    template_name = "accounts/login.html"
    login_form_class = LoginForm
    signup_form_class = SignUpForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next") or reverse_lazy("video_summary:main")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("video_summary:main")

        return super().dispatch(request, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "login_form": self.login_form_class(),
                "signup_form": self.signup_form_class(),
                "show_signup": True,  # Show signup form by default
            },
        )

    def post(self, request, *args, **kwargs):
        signup_form = self.signup_form_class(request.POST)

        if signup_form.is_valid():
            cleaned_data = signup_form.cleaned_data
            if User.objects.filter(username=cleaned_data["username"]).exists():
                messages.error(
                    request,
                    "نام کاربری مورد نظر در دسترس نمی‌باشد",
                    "text-red-700 bg-red-300 border-red-400",
                )
                return render(
                    request,
                    self.template_name,
                    {
                        "login_form": self.login_form_class(),
                        "signup_form": signup_form,
                        "show_signup": True,
                    },
                )
            user = User.objects.create_user(
                username=cleaned_data["username"],
                password=cleaned_data["password"],
                email=cleaned_data["email"],
            )
            login(request, user)
            messages.success(
                request,
                "حساب کاربری شما با موفقیت ساخته شد",
                "text-green-700 bg-green-300 border-green-400",
            )
            return redirect(self.next)
        return render(
            request,
            self.template_name,
            {
                "signup_form": signup_form,
                "login_form": self.login_form_class(),
                "show_signup": True,
            },
        )


class LogoutView(View):
    success_url = reverse_lazy("video_summary:main")

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)


class RecoveryPasswordView(View):
    template_name = "accounts/recovery_password.html"
    recovery_password_form = RecoveryPasswordForm
    verify_otp_form = VerifyOTPForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "recovery_password_form": self.recovery_password_form(),
                "verify_otp_form": self.verify_otp_form(),
            },
        )

    def post(self, request, *args, **kwargs):
        recovery_password_form = self.recovery_password_form(request.POST)
        if recovery_password_form.is_valid():
            username_email = recovery_password_form.cleaned_data["username_email"]
            otp = generate_otp(username_email)

            # Send OTP via email (replace with your email sending logic)
            send_mail(
                "OTP Code",
                f"Your OTP code is: {otp}",
                "from@example.com",
                [username_email],  # Assuming username_email is the user's email
                fail_silently=False,
            )

            # Return success response
            return JsonResponse(
                {
                    "success": True,
                    "username_email": username_email,
                }
            )
        else:
            # Return error response
            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid input. Please check your username/email.",
                }
            )


class VerifyOTPView(View):
    verify_otp_form = VerifyOTPForm

    def post(self, request, *args, **kwargs):
        verify_otp_form = self.verify_otp_form(request.POST)
        if verify_otp_form.is_valid():
            username_email = verify_otp_form.cleaned_data["username_email"]
            code = verify_otp_form.cleaned_data["code"]

            # Verify OTP
            if verify_otp(username_email, code):
                return JsonResponse({"success": True})
            else:
                return JsonResponse(
                    {"success": False, "error": "Invalid or expired OTP."}
                )
        else:
            return JsonResponse(
                {"success": False, "error": "Invalid input. Please check your OTP."}
            )
