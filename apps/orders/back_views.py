from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from apps.billing.services import InvoiceService

from .models import Order, Payment


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("orders.view_order", raise_exception=True), name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "backoffice/orders/list.html"
    context_object_name = "orders"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("orders.view_order", raise_exception=True), name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "backoffice/orders/detail.html"
    context_object_name = "order"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("orders.change_order", raise_exception=True), name="dispatch")
class OrderRefundView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        order = get_object_or_404(Order, pk=pk)
        payment = order.payments.filter(status=Payment.Status.CAPTURED).first()
        if payment:
            payment.status = Payment.Status.REFUNDED
            payment.save(update_fields=["status"])
            order.status = Order.Status.CANCELED
            order.save(update_fields=["status"])
            InvoiceService().generate_credit_note(order)
            messages.success(request, "Commande remboursée")
        return redirect("back:orders:detail", pk=order.pk)
