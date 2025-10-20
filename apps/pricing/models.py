from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class PriceRule(TimeStampedModel):
    class AppliesTo(models.TextChoices):
        SERVICE = "service", "Service"
        PRODUCT = "product", "Produit"

    class RuleType(models.TextChoices):
        FIXED = "fixed", "Montant fixe"
        PERCENT = "percent", "Pourcentage"
        TIER = "tier", "Palier"

    name = models.CharField(max_length=255)
    applies_to = models.CharField(max_length=20, choices=AppliesTo.choices)
    target_id = models.PositiveIntegerField()
    rule_type = models.CharField(max_length=20, choices=RuleType.choices)
    value = models.JSONField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.applies_to})"

    def is_active(self, at: timezone.datetime | None = None) -> bool:
        at = at or timezone.now()
        if self.start_at > at:
            return False
        if self.end_at and self.end_at < at:
            return False
        return True

    def compute(self, base_price: float, quantity: int = 1) -> float:
        if self.rule_type == self.RuleType.FIXED:
            return float(self.value)
        if self.rule_type == self.RuleType.PERCENT:
            return base_price * (1 - float(self.value) / 100)
        if self.rule_type == self.RuleType.TIER:
            tiers = sorted(self.value, key=lambda tier: tier["min_qty"])
            price = base_price
            for tier in tiers:
                if quantity >= tier["min_qty"]:
                    price = tier["price"]
            return float(price)
        return base_price
