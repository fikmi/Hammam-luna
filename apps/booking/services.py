from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.billing.services import InvoiceService
from apps.catalog.models import Service
from apps.orders.models import Order, Payment
from apps.people.models import Provider, ProviderAvailability, ProviderTimeOff

from .models import Appointment


class AppointmentService:
    cancellation_window_hours = 24
    no_show_fee = Decimal("20.00")

    def availability(self, service: Service, days: int = 14) -> dict[str, list[dict[str, object]]]:
        slots: dict[str, list[dict[str, object]]] = defaultdict(list)
        providers = service.available_providers()
        for provider in providers:
            for day_offset in range(days):
                date = timezone.localdate() + timedelta(days=day_offset)
                for availability in ProviderAvailability.objects.filter(provider=provider, weekday=date.weekday()):
                    start_dt = datetime.combine(date, availability.start_hour, tzinfo=timezone.get_current_timezone())
                    end_dt = datetime.combine(date, availability.end_hour, tzinfo=timezone.get_current_timezone())
                    slot_start = start_dt
                    while slot_start + timedelta(minutes=service.duration_min) <= end_dt:
                        slot_end = slot_start + timedelta(minutes=service.duration_min)
                        if not self._has_overlap(provider, slot_start, slot_end):
                            slots[str(date)].append({"provider": provider, "start": slot_start})
                        slot_start += timedelta(minutes=service.duration_min)
        return slots

    def _has_overlap(self, provider: Provider, start: datetime, end: datetime) -> bool:
        if ProviderTimeOff.objects.filter(provider=provider, start_at__lte=end, end_at__gte=start).exists():
            return True
        return Appointment.objects.filter(provider=provider, start_at__lt=end, end_at__gt=start).exists()

    def book(self, customer, service: Service, provider: Provider, start: datetime, notes: str = "") -> Appointment:
        end = start + timedelta(minutes=service.duration_min)
        if self._has_overlap(provider, start, end):
            raise ValueError("Créneau indisponible")
        appointment = Appointment.objects.create(
            customer=customer,
            service=service,
            provider=provider,
            start_at=start,
            end_at=end,
            status=Appointment.Status.CONFIRMED,
            notes=notes,
        )
        return appointment

    def cancel(self, appointment: Appointment) -> Appointment:
        appointment.status = Appointment.Status.CANCELED
        appointment.save(update_fields=["status"])
        return appointment

    @transaction.atomic
    def mock_payment(self, order: Order, method: str) -> Payment:
        order.status = Order.Status.PAID
        order.total = order.items.aggregate(total=Sum("total"))["total"] or Decimal("0.00")
        order.save(update_fields=["status", "total"])
        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.total,
            status=Payment.Status.CAPTURED,
            txn_ref=f"MOCK-{order.pk}",
            paid_at=timezone.now(),
        )
        InvoiceService().generate_invoice(order)
        return payment

    def get(self, appointment_id: int) -> Appointment:
        return Appointment.objects.get(pk=appointment_id)
