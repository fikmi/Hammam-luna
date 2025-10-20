from __future__ import annotations

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import TwoFactorProfile
from .otp import TOTP

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class TwoFactorForm(forms.Form):
    token = forms.CharField(label="Code", max_length=6)

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_token(self) -> str:
        token = self.cleaned_data["token"]
        profile = TwoFactorProfile.objects.get(user=self.user)
        totp = TOTP(profile.secret)
        if not totp.verify(token, valid_window=1):
            raise forms.ValidationError("Code invalide")
        return token


class TwoFactorSetupForm(forms.ModelForm):
    class Meta:
        model = TwoFactorProfile
        fields = ("enabled",)


class SessionAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if getattr(user, "is_active", False) is False:
            raise forms.ValidationError("Compte inactif", code="inactive")


class EmailAuthenticationForm(SessionAuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Identifiants invalides")
            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Identifiants invalides")
        return self.cleaned_data
