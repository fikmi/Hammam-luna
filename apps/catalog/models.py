from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel


class Service(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_min = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    provider = models.ForeignKey("people.Provider", null=True, blank=True, on_delete=models.SET_NULL, related_name="services")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def available_providers(self):
        from apps.people.models import Provider

        if self.provider:
            return Provider.objects.filter(pk=self.provider.pk, is_active=True)
        return Provider.objects.filter(is_active=True)


class Product(TimeStampedModel):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_qty = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def in_stock(self) -> bool:
        return self.stock_qty > 0
