from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditLog(TimeStampedModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    entity = models.CharField(max_length=255)
    entity_id = models.CharField(max_length=255)
    payload = models.JSONField(default=dict, blank=True)
    at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-at"]

    def __str__(self) -> str:
        return f"{self.actor} {self.action} {self.entity}#{self.entity_id}"


class SiteSetting(TimeStampedModel):
    key = models.CharField(max_length=255, unique=True)
    value = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.key}"


class TwoFactorProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="two_factor")
    secret = models.CharField(max_length=32, blank=True)
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"2FA profile for {self.user}"
