from __future__ import annotations

from datetime import time

import pytest
from django.utils import timezone

from apps.booking.services import AppointmentService
from apps.people.models import ProviderAvailability
from factories import AppointmentFactory, CustomerFactory, ServiceFactory


@pytest.mark.django_db
def test_availability_respects_existing_appointment():
    appointment = AppointmentFactory()
    ProviderAvailability.objects.create(
        provider=appointment.provider,
        weekday=appointment.start_at.weekday(),
        start_hour=appointment.start_at.time(),
        end_hour=(appointment.start_at + timezone.timedelta(hours=2)).time(),
    )
    slots = AppointmentService().availability(appointment.service, days=1)
    assert str(appointment.start_at.date()) not in slots


@pytest.mark.django_db
def test_booking_creates_appointment():
    customer = CustomerFactory()
    service = ServiceFactory()
    ProviderAvailability.objects.create(provider=service.provider, weekday=timezone.now().weekday(), start_hour=time(9, 0), end_hour=time(18, 0))
    start = timezone.now() + timezone.timedelta(days=1)
    appointment = AppointmentService().book(customer, service, service.provider, start)
    assert appointment.pk is not None
    assert appointment.status == appointment.Status.CONFIRMED
