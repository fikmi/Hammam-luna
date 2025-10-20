from __future__ import annotations

import random
from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.booking.models import Appointment
from apps.catalog.models import Product, Service
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem
from apps.people.models import Provider, ProviderAvailability
from apps.pricing.models import PriceRule

User = get_user_model()


class Command(BaseCommand):
    help = "Crée des données de démonstration"

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(username="owner", defaults={"email": "owner@example.com"})
        owner.set_password("demo1234")
        owner.save()

        providers = []
        for name in ["Aïcha", "Youssef"]:
            provider, _ = Provider.objects.get_or_create(name=name, contact_email=f"{name.lower()}@example.com")
            ProviderAvailability.objects.get_or_create(provider=provider, weekday=0, start_hour=time(9, 0), end_hour=time(17, 0))
            ProviderAvailability.objects.get_or_create(provider=provider, weekday=2, start_hour=time(9, 0), end_hour=time(17, 0))
            providers.append(provider)

        services = []
        for idx, name in enumerate(["Massage relaxant", "Hammam traditionnel", "Gommage oriental", "Soins visage", "Rituel duo"]):
            service, _ = Service.objects.get_or_create(
                name=name,
                defaults={
                    "description": "Un moment de détente unique.",
                    "duration_min": 60,
                    "base_price": 80 + idx * 10,
                    "provider": random.choice(providers),
                },
            )
            services.append(service)

        products = []
        for idx in range(1, 9):
            product, _ = Product.objects.get_or_create(
                sku=f"P{idx:03d}",
                defaults={
                    "name": f"Huile parfumée {idx}",
                    "description": "Huile aromatique",
                    "price": 30 + idx,
                    "stock_qty": 50,
                },
            )
            products.append(product)

        customers = []
        for idx in range(1, 4):
            user, _ = User.objects.get_or_create(username=f"client{idx}", defaults={"email": f"client{idx}@example.com"})
            user.set_password("demo1234")
            user.save()
            customer, _ = Customer.objects.get_or_create(user=user, email=user.email, defaults={"first_name": f"Client {idx}"})
            customers.append(customer)

        PriceRule.objects.get_or_create(
            name="Promo massage",
            applies_to=PriceRule.AppliesTo.SERVICE,
            target_id=services[0].pk,
            defaults={
                "rule_type": PriceRule.RuleType.PERCENT,
                "value": 10,
                "start_at": timezone.now() - timedelta(days=1),
                "end_at": timezone.now() + timedelta(days=30),
            },
        )

        for customer in customers:
            order, _ = Order.objects.get_or_create(customer=customer, status=Order.Status.PAID, defaults={"total": 0})
            total = 0
            for item in random.sample(products, 2):
                qty = random.randint(1, 3)
                total += item.price * qty
                OrderItem.objects.get_or_create(
                    order=order,
                    kind=OrderItem.Kind.PRODUCT,
                    ref_id=item.pk,
                    defaults={
                        "name": item.name,
                        "qty": qty,
                        "unit_price": item.price,
                        "total": item.price * qty,
                    },
                )
            order.total = total
            order.save()

        for customer in customers:
            service = random.choice(services)
            start = timezone.now() + timedelta(days=random.randint(1, 10))
            Appointment.objects.get_or_create(
                customer=customer,
                service=service,
                provider=service.provider,
                start_at=start,
                end_at=start + timedelta(minutes=service.duration_min),
                defaults={"status": Appointment.Status.CONFIRMED},
            )

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées."))
