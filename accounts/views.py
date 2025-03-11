from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from accounts.forms import LoginForm, SignUpForm, RecoveryPasswordForm, SetPasswordForm
from django.contrib import messages
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Q
from utils import MessageStatus
from django.contrib.auth.views import PasswordResetConfirmView


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
                    MessageStatus.SUCCESS.value,
                )
                return redirect(self.next)
            messages.error(
                request,
                "نام کاربری یا رمزعبور صحیح نمی‌باشد",
                MessageStatus.ERROR.value,
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
                    MessageStatus.ERROR.value,
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
                MessageStatus.SUCCESS.value,
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

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "recovery_password_form": self.recovery_password_form(),
            },
        )

    def post(self, request, *args, **kwargs):
        recovery_password_form = self.recovery_password_form(request.POST)
        if recovery_password_form.is_valid():
            username_email = recovery_password_form.cleaned_data["username_email"]
            user = User.objects.get(
                Q(username=username_email) | Q(email=username_email)
            )
            if user.email:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                url = reverse_lazy(
                    "accounts:set_password", kwargs={"uidb64": uid, "token": token}
                )
                send_mail(
                    "Reset Password",
                    f"Your Reset password link: {url}",
                    "test@test.com",
                    [user.email],  # Assuming username_email is the user's email
                    fail_silently=False,
                )

            # Return success response
            messages.success(
                request,
                message="""ما دستورالعمل‌های تنظیم رمز عبور را برای شما ایمیل کرده‌ایم، در صورتی که حسابی با ایمیل وارد شده وجود داشته باشد. شما باید به‌زودی این ایمیل را دریافت کنید.
اگر ایمیلی دریافت نکردید، لطفاً مطمئن شوید که آدرس ایمیلی که ثبت‌نام کرده‌اید را وارد کرده‌اید و پوشه اسپم (هرزنامه) خود را نیز بررسی کنید.""",
                extra_tags=MessageStatus.SUCCESS.value,
            )
            return render(
                request,
                self.template_name,
                {"recovery_password_form": recovery_password_form},
            )


class SetPasswordView(PasswordResetConfirmView):
    template_name = "accounts/set_password.html"
    success_url = reverse_lazy("video_summary:main")
    form_class = SetPasswordForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "رمز عبور شما با موفقیت تغییر یافت. اکنون می‌توانید وارد شوید.",
            extra_tags=MessageStatus.SUCCESS.value,
        )
        return super().form_valid(form)
