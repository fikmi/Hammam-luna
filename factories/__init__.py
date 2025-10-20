from __future__ import annotations

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.booking.models import Appointment
from apps.catalog.models import Product, Service
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem
from apps.people.models import Provider
from apps.pricing.models import PriceRule

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Sequence(lambda n: f"Provider {n}")
    contact_email = factory.LazyAttribute(lambda obj: f"provider{obj.id or 0}@example.com")


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.Sequence(lambda n: f"Service {n}")
    description = "Description"
    duration_min = 60
    base_price = 80
    provider = factory.SubFactory(ProviderFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    sku = factory.Sequence(lambda n: f"SKU{n}")
    name = factory.Sequence(lambda n: f"Produit {n}")
    description = "Produit"
    price = 30
    stock_qty = 10


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: obj.user.email)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    status = Order.Status.PAID
    total = 0


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    kind = OrderItem.Kind.PRODUCT
    ref_id = factory.Sequence(lambda n: n + 1)
    name = "Produit"
    qty = 1
    unit_price = 30
    total = 30


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    customer = factory.SubFactory(CustomerFactory)
    service = factory.SubFactory(ServiceFactory)
    provider = factory.LazyAttribute(lambda obj: obj.service.provider)
    start_at = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=1))
    end_at = factory.LazyAttribute(lambda obj: obj.start_at + timezone.timedelta(minutes=obj.service.duration_min))
    status = Appointment.Status.CONFIRMED


class PriceRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PriceRule

    name = factory.Sequence(lambda n: f"Rule {n}")
    applies_to = PriceRule.AppliesTo.SERVICE
    target_id = factory.Sequence(lambda n: n + 1)
    rule_type = PriceRule.RuleType.PERCENT
    value = 10
    start_at = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=1))
    end_at = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=1))

    @factory.post_generation
    def bind_service(self, create, extracted, **kwargs):
        if extracted:
            self.applies_to = PriceRule.AppliesTo.SERVICE
            self.target_id = extracted.pk
            if create:
                self.save(update_fields=["applies_to", "target_id"])
