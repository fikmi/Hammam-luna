from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        CART = "cart", "Panier"
        PENDING = "pending", "En attente"
        PAID = "paid", "Payée"
        SHIPPED = "shipped", "Expédiée"
        COMPLETED = "completed", "Terminée"
        CANCELED = "canceled", "Annulée"

    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CART)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField(max_length=10, default="EUR")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Commande #{self.pk}"

    def recalculate(self) -> None:
        total = self.items.aggregate(total=models.Sum("total"))["total"] or Decimal("0.00")
        self.total = total
        self.save(update_fields=["total"])


class OrderItem(TimeStampedModel):
    class Kind(models.TextChoices):
        SERVICE = "service", "Service"
        PRODUCT = "product", "Produit"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    kind = models.CharField(max_length=20, choices=Kind.choices)
    ref_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self) -> str:
        return f"{self.name} x{self.qty}"


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CARD = "card", "Carte"
        CASH = "cash", "Espèces"
        TRANSFER = "transfer", "Virement"

    class Status(models.TextChoices):
        AUTHORIZED = "authorized", "Autorisé"
        CAPTURED = "captured", "Capturé"
        FAILED = "failed", "Echoué"
        REFUNDED = "refunded", "Remboursé"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices)
    txn_ref = models.CharField(max_length=255, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Paiement {self.method} - {self.status}"
