from __future__ import annotations

from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmailAuthenticationForm, RegistrationForm, TwoFactorForm, TwoFactorSetupForm
from .models import TwoFactorProfile
from .otp import random_base32


class EmailLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "auth/login.html"

    def form_valid(self, form):
        user = form.get_user()
        if user and getattr(user, "two_factor", None) and user.two_factor.enabled:
            self.request.session["_2fa_user_id"] = user.pk
            return redirect("account_two_factor_verify")
        login(self.request, user)
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            raw_password = form.cleaned_data.get("password1")
            auth_user = authenticate(username=user.username, password=raw_password)
            login(request, auth_user)
            messages.success(request, "Compte créé avec succès")
            return redirect("front:home")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "Vous êtes déconnecté")
    return redirect("front:home")


@login_required
def two_factor(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(TwoFactorProfile, user=request.user)
    if request.method == "POST":
        form = TwoFactorSetupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres 2FA mis à jour")
            return redirect("dashboard:index")
    else:
        if not profile.secret:
            profile.secret = random_base32()
            profile.save(update_fields=["secret"])
        form = TwoFactorSetupForm(instance=profile)
    identifier = request.user.email or request.user.username
    issuer = "Hammam Luna"
    otpauth_uri = f"otpauth://totp/{quote(issuer)}:{quote(identifier)}?secret={profile.secret}&issuer={quote(issuer)}"
    return render(request, "auth/two_factor_setup.html", {"form": form, "uri": otpauth_uri, "secret": profile.secret})


def two_factor_challenge(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get("_2fa_user_id")
    profile = get_object_or_404(TwoFactorProfile, user_id=user_id)
    if request.method == "POST":
        form = TwoFactorForm(profile.user, request.POST)
        if form.is_valid():
            login(request, profile.user)
            request.session.pop("_2fa_user_id", None)
            messages.success(request, "Connexion réussie")
            return redirect("dashboard:index")
    else:
        form = TwoFactorForm(profile.user)
    return render(request, "auth/two_factor_verify.html", {"form": form})
