from __future__ import annotations

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .forms import PriceRuleForm
from .models import PriceRule


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("pricing.view_pricerule", raise_exception=True), name="dispatch")
class PriceRuleListView(ListView):
    model = PriceRule
    template_name = "backoffice/pricing/list.html"
    context_object_name = "rules"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("pricing.add_pricerule", raise_exception=True), name="dispatch")
class PriceRuleCreateView(CreateView):
    model = PriceRule
    form_class = PriceRuleForm
    template_name = "backoffice/pricing/form.html"
    success_url = "/backoffice/pricing/"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("pricing.change_pricerule", raise_exception=True), name="dispatch")
class PriceRuleUpdateView(UpdateView):
    model = PriceRule
    form_class = PriceRuleForm
    template_name = "backoffice/pricing/form.html"
    success_url = "/backoffice/pricing/"
