from __future__ import annotations

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from apps.orders.cart import Cart
from apps.orders.forms import CheckoutForm
from apps.orders.models import Payment
from factories import CustomerFactory, ProductFactory, ServiceFactory


@pytest.mark.django_db
def test_cart_to_order_and_payment():
    request = RequestFactory().get("/")
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    cart = Cart.for_request(request)
    product = ProductFactory(price=50)
    service = ServiceFactory(base_price=100)
    cart.add_product(product)
    cart.add_service(service)

    customer = CustomerFactory()
    order = cart.to_order(customer)
    assert order.items.count() == 2

    form = CheckoutForm(data={"payment_method": Payment.Method.CARD})
    assert form.is_valid()

    from apps.booking.services import AppointmentService

    payment = AppointmentService().mock_payment(order, form.cleaned_data["payment_method"])
    order.refresh_from_db()
    assert payment.status == Payment.Status.CAPTURED
    assert order.status == order.Status.PAID
