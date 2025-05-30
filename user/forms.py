from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLogInForm(AuthenticationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError(_("Invalid email or password"))

        return cleaned_data

    def get_user(self):
        return self.user
