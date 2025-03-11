from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm


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


class SetPasswordForm(DjangoSetPasswordForm):
    error_messages = {
        "password_mismatch": "رمز عبور و تأیید آن یکسان نیستند.",
        "password_too_similar": "رمز عبور بیش از حد شبیه به نام کاربری است.",
        "password_too_short": "رمز عبور خیلی کوتاه است. حداقل باید ۸ کاراکتر داشته باشد.",
        "password_too_common": "این رمز عبور خیلی رایج است.",
        "password_entirely_numeric": "رمز عبور نباید فقط شامل اعداد باشد.",
    }

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور جدید"}
        ),
        label="رمز عبور جدید",
        error_messages={"required": "لطفاً رمز عبور جدید خود را وارد کنید."},
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "تأیید رمز عبور"}
        ),
        label="تأیید رمز عبور",
        error_messages={"required": "لطفاً رمز عبور خود را تأیید کنید."},
    )
