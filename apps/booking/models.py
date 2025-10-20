from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class Appointment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CONFIRMED = "confirmed", "Confirmé"
        DONE = "done", "Terminé"
        NO_SHOW = "no_show", "Absent"
        CANCELED = "canceled", "Annulé"

    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey("catalog.Service", on_delete=models.CASCADE, related_name="appointments")
    provider = models.ForeignKey("people.Provider", on_delete=models.CASCADE, related_name="appointments")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_at"]
        unique_together = ("provider", "start_at")

    def __str__(self) -> str:
        return f"{self.service} - {self.start_at:%d/%m %H:%M}"

    def overlaps(self, start: timezone.datetime, end: timezone.datetime) -> bool:
        return not (end <= self.start_at or start >= self.end_at)

    @property
    def duration(self) -> timedelta:
        return self.end_at - self.start_at
