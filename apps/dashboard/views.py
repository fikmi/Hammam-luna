from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.booking.models import Appointment
from apps.orders.models import Order, OrderItem


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("orders.view_order", raise_exception=True), name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        orders = Order.objects.filter(created_at__gte=thirty_days_ago, status__in=[Order.Status.PAID, Order.Status.COMPLETED])
        revenue = orders.aggregate(total=Sum("total"))["total"] or 0
        avg_cart = orders.aggregate(avg=Avg("total"))["avg"] or 0
        total_appointments = Appointment.objects.count() or 1
        no_show_rate = (Appointment.objects.filter(status=Appointment.Status.NO_SHOW).count() / total_appointments) * 100
        provider_occupation = (
            Appointment.objects.filter(status=Appointment.Status.CONFIRMED)
            .values("provider__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        top_services = (
            OrderItem.objects.filter(kind=OrderItem.Kind.SERVICE)
            .values("name")
            .annotate(total_qty=Sum("qty"))
            .order_by("-total_qty")[:5]
        )
        top_products = (
            OrderItem.objects.filter(kind=OrderItem.Kind.PRODUCT)
            .values("name")
            .annotate(total_qty=Sum("qty"))
            .order_by("-total_qty")[:5]
        )
        context.update(
            {
                "revenue": revenue,
                "avg_cart": avg_cart,
                "no_show_rate": no_show_rate,
                "provider_occupation": provider_occupation,
                "top_services": top_services,
                "top_products": top_products,
                "orders": orders,
            }
        )
        return context
