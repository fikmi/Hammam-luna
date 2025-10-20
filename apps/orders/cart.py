from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from django.http import HttpRequest

from apps.catalog.models import Product, Service
from apps.customers.models import Customer
from apps.pricing.services import PricingEngine

from .models import Order, OrderItem


@dataclass
class CartItem:
    key: str
    name: str
    qty: int
    price: Decimal
    kind: str
    ref_id: int

    @property
    def total(self) -> Decimal:
        return self.price * self.qty


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request: HttpRequest):
        self.request = request
        self.session = request.session
        self.data: Dict[str, dict] = dict(self.session.get(self.SESSION_KEY, {}))

    @classmethod
    def for_request(cls, request: HttpRequest) -> "Cart":
        return cls(request)

    def add_service(self, service: Service, qty: int = 1) -> None:
        pricing = PricingEngine().for_service(service, qty)
        key = f"service:{service.pk}"
        self.data[key] = {"name": service.name, "qty": qty, "price": float(pricing), "kind": "service", "ref_id": service.pk}
        self._persist()

    def add_product(self, product: Product, qty: int = 1) -> None:
        pricing = PricingEngine().for_product(product, qty)
        key = f"product:{product.pk}"
        self.data[key] = {"name": product.name, "qty": qty, "price": float(pricing), "kind": "product", "ref_id": product.pk}
        self._persist()

    def remove(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
            self._persist()

    @property
    def items(self) -> list[CartItem]:
        return [CartItem(key=k, name=v["name"], qty=v["qty"], price=Decimal(str(v["price"])), kind=v["kind"], ref_id=v["ref_id"]) for k, v in self.data.items()]

    @property
    def total(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal("0.00"))

    def clear(self) -> None:
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def _persist(self) -> None:
        self.session[self.SESSION_KEY] = self.data
        self.session.modified = True

    def to_order(self, customer: Customer) -> Order:
        order = Order.objects.create(customer=customer, status=Order.Status.PENDING, total=self.total)
        for item in self.items:
            OrderItem.objects.create(
                order=order,
                kind=item.kind,
                ref_id=item.ref_id,
                name=item.name,
                qty=item.qty,
                unit_price=item.price,
                total=item.total,
            )
        self.clear()
        return order
