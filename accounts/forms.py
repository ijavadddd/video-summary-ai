from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""  # Remove the colon
        super().__init__(*args, **kwargs)

    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="رمزعبور")


class SignUpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""  # Remove the colon
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label="نام کاربری", widget=forms.TextInput(attrs={"id": "signup-username"})
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.TextInput(attrs={"id": "signup-email"}),
        error_messages={
            "required": "این فیلد الزامی است",
            "invalid": "لطفاً یک ایمیل معتبر وارد کنید",
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "signup-password"}), label="رمزعبور"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "signup-confirm-password"}),
        label="تکرار رمزعبور",
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("رمزعبور و تکرار آن مطابقت ندارد")
        return confirm_password


class RecoveryPasswordForm(forms.Form):
    username_email = forms.CharField(
        label="نام کاربری یا ایمیل",
        label_suffix="",
        widget=forms.TextInput(
            attrs={"placeholder": "نام کاربری یا ایمیل خود را وارد کنید"}
        ),
    )


class VerifyOTPForm(forms.Form):
    username_email = forms.CharField(
        label="نام کاربری یا ایمیل",
        label_suffix="",
        widget=forms.TextInput(attrs={"readonly": ""}),
    )
    code = forms.CharField(
        label="رمز یکبار مصرف",
        label_suffix="",
        widget=forms.TextInput(
            attrs={"placeholder": "رمز یکبار مصرف ارسال شده به ایمیل خو را وارد کنید"}
        ),
    )
