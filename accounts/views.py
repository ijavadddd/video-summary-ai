from django.shortcuts import render
from django.views.generic import View
from accounts.forms import LoginForm, SignUpForm


class LoginView(View):
    template_name = "accounts/login.html"
    login_form_class = LoginForm
    signup_form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "login_form": self.login_form_class(),
                "signup_form": self.signup_form_class(),
            },
        )
