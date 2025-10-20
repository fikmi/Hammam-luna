from __future__ import annotations

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ProviderForm
from .models import Provider


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("people.view_provider", raise_exception=True), name="dispatch")
class ProviderListView(ListView):
    model = Provider
    template_name = "backoffice/providers/list.html"
    context_object_name = "providers"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("people.add_provider", raise_exception=True), name="dispatch")
class ProviderCreateView(CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = "backoffice/providers/form.html"
    success_url = "/backoffice/providers/"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("people.change_provider", raise_exception=True), name="dispatch")
class ProviderUpdateView(UpdateView):
    model = Provider
    form_class = ProviderForm
    template_name = "backoffice/providers/form.html"
    success_url = "/backoffice/providers/"
