from __future__ import annotations

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ServiceForm
from .models import Service


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.view_service", raise_exception=True), name="dispatch")
class ServiceListView(ListView):
    model = Service
    template_name = "backoffice/services/list.html"
    context_object_name = "services"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.add_service", raise_exception=True), name="dispatch")
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "backoffice/services/form.html"
    success_url = "/backoffice/services/"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.change_service", raise_exception=True), name="dispatch")
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "backoffice/services/form.html"
    success_url = "/backoffice/services/"
