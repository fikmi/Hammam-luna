from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from django.utils import timezone

from apps.catalog.models import Product, Service

from .models import PriceRule


class PricingEngine:
    def _rules_for(self, applies_to: str, target_id: int) -> Iterable[PriceRule]:
        now = timezone.now()
        return PriceRule.objects.filter(applies_to=applies_to, target_id=target_id).order_by("start_at")

    def for_service(self, service: Service, quantity: int = 1) -> Decimal:
        price = Decimal(service.base_price)
        for rule in self._rules_for(PriceRule.AppliesTo.SERVICE, service.pk):
            if rule.is_active():
                price = Decimal(rule.compute(float(price), quantity))
        return price

    def for_product(self, product: Product, quantity: int = 1) -> Decimal:
        price = Decimal(product.price)
        for rule in self._rules_for(PriceRule.AppliesTo.PRODUCT, product.pk):
            if rule.is_active():
                price = Decimal(rule.compute(float(price), quantity))
        return price

    def apply_to_order_item(self, item) -> None:
        if item.kind == "service":
            item.unit_price = self.for_service(Service.objects.get(pk=item.ref_id), item.qty)
        else:
            item.unit_price = self.for_product(Product.objects.get(pk=item.ref_id), item.qty)
        item.total = item.unit_price * item.qty
