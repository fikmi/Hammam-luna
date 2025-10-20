from __future__ import annotations

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView

from .models import Appointment
from .services import AppointmentService


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("booking.view_appointment", raise_exception=True), name="dispatch")
class AppointmentCalendarView(TemplateView):
    template_name = "backoffice/booking/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.request.GET.get("service")
        if service_id:
            appointment = Appointment.objects.filter(service_id=service_id).first()
            if appointment:
                context["availability"] = AppointmentService().availability(appointment.service)
        context["appointments"] = Appointment.objects.select_related("service", "provider", "customer").all()
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("booking.change_appointment", raise_exception=True), name="dispatch")
class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ("status", "notes")
    template_name = "backoffice/booking/form.html"
    success_url = "/backoffice/booking/"
