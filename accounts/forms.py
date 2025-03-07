from django import forms


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
        label="ایمیل", widget=forms.TextInput(attrs={"id": "signup-email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "signup-password"}), label="رمزعبور"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "signup-confirm-password"}),
        label="تکرار رمزعبور",
    )
