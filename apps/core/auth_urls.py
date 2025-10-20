from __future__ import annotations

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import EmailLoginView, logout_view, register, two_factor, two_factor_challenge

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="account_login"),
    path("logout/", logout_view, name="account_logout"),
    path("register/", register, name="account_register"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="auth/password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"), name="password_reset_complete"),
    path("two-factor/", two_factor, name="account_two_factor"),
    path("two-factor/verify/", two_factor_challenge, name="account_two_factor_verify"),
]
