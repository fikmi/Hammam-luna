from __future__ import annotations

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .forms import ProductForm
from .models import Product


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.view_product", raise_exception=True), name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "backoffice/products/list.html"
    context_object_name = "products"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.add_product", raise_exception=True), name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "backoffice/products/form.html"
    success_url = "/backoffice/products/"


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required("catalog.change_product", raise_exception=True), name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "backoffice/products/form.html"
    success_url = "/backoffice/products/"
