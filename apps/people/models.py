from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Staff(TimeStampedModel):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Propriétaire"
        STAFF = "STAFF", "Equipe"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user} ({self.role})"


class Provider(TimeStampedModel):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    skills = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class ProviderAvailability(TimeStampedModel):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="availabilities")
    weekday = models.IntegerField(help_text="0=lundi")
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        ordering = ["provider", "weekday", "start_hour"]

    def __str__(self) -> str:
        return f"{self.provider} - {self.weekday} {self.start_hour}-{self.end_hour}"


class ProviderTimeOff(TimeStampedModel):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="exclusions")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Indisponibilité"
        verbose_name_plural = "Indisponibilités"
        ordering = ["-start_at"]

    def __str__(self) -> str:
        return f"{self.provider} indispo {self.start_at}-{self.end_at}"
