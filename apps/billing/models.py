from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class Invoice(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="invoice")
    pdf = models.FileField(upload_to="invoices/")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="EUR")

    def __str__(self) -> str:
        return f"Facture {self.order_id}"


class CreditNote(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="credit_note")
    pdf = models.FileField(upload_to="credit_notes/")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Avoir {self.order_id}"
