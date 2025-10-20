from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.booking.forms import AppointmentForm
from apps.booking.services import AppointmentService
from apps.catalog.models import Product, Service
from apps.customers.forms import CustomerProfileForm
from apps.customers.models import Customer
from apps.orders.cart import Cart
from apps.orders.forms import CheckoutForm
from apps.orders.models import Order
from apps.pricing.services import PricingEngine


def home(request: HttpRequest) -> HttpResponse:
    services = Service.objects.filter(is_active=True).order_by("name")[:6]
    products = Product.objects.filter(is_active=True).order_by("name")[:6]
    return render(request, "front/home.html", {"services": services, "products": products})


def service_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q")
    services = Service.objects.filter(is_active=True)
    if query:
        services = services.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, "front/services_list.html", {"services": services, "query": query})


def service_detail(request: HttpRequest, pk: int) -> HttpResponse:
    service = get_object_or_404(Service, pk=pk, is_active=True)
    providers = service.available_providers()
    pricing = PricingEngine().for_service(service)
    return render(request, "front/service_detail.html", {"service": service, "providers": providers, "pricing": pricing})


def product_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q")
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, "front/products_list.html", {"products": products, "query": query})


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, is_active=True)
    pricing = PricingEngine().for_product(product)
    return render(request, "front/product_detail.html", {"product": product, "pricing": pricing})


@login_required
@transaction.atomic
def appointment_booking(request: HttpRequest, service_id: int) -> HttpResponse:
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    customer, _ = Customer.objects.get_or_create(user=request.user, defaults={
        "first_name": request.user.first_name or request.user.username,
        "last_name": request.user.last_name or "",
        "email": request.user.email or "",
    })
    if request.method == "POST":
        form = AppointmentForm(service, customer, request.POST)
        if form.is_valid():
            appointment = AppointmentService().book(
                customer=customer,
                service=service,
                provider=form.cleaned_data["provider"],
                start=form.cleaned_data["start_at"],
                notes=form.cleaned_data.get("notes", ""),
            )
            messages.success(request, "Rendez-vous confirmé")
            return redirect("front:appointment_confirm", appointment_id=appointment.pk)
    else:
        form = AppointmentForm(service, customer)
    availability = AppointmentService().availability(service, days=14)
    return render(request, "front/appointment_booking.html", {"service": service, "form": form, "availability": availability})


def appointment_confirm(request: HttpRequest, appointment_id: int) -> HttpResponse:
    appointment = AppointmentService().get(appointment_id)
    return render(request, "front/appointment_confirm.html", {"appointment": appointment})


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = Cart.for_request(request)
    return render(request, "front/cart.html", {"cart": cart})


def cart_add_service(request: HttpRequest, service_id: int) -> HttpResponse:
    service = get_object_or_404(Service, pk=service_id)
    Cart.for_request(request).add_service(service)
    messages.success(request, f"{service.name} ajouté au panier")
    return redirect("front:cart")


def cart_add_product(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    Cart.for_request(request).add_product(product)
    messages.success(request, f"{product.name} ajouté au panier")
    return redirect("front:cart")


def cart_remove(request: HttpRequest, item_id: str) -> HttpResponse:
    Cart.for_request(request).remove(item_id)
    return redirect("front:cart")


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart = Cart.for_request(request)
    customer, _ = Customer.objects.get_or_create(user=request.user, defaults={
        "first_name": request.user.first_name or request.user.username,
        "last_name": request.user.last_name or "",
        "email": request.user.email or "",
    })
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = cart.to_order(customer)
            AppointmentService().mock_payment(order, form.cleaned_data["payment_method"])
            messages.success(request, "Paiement confirmé")
            return redirect("front:order_detail", order_id=order.pk)
    else:
        form = CheckoutForm()
    return render(request, "front/checkout.html", {"cart": cart, "form": form})


@login_required
def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=order_id, customer__user=request.user)
    return render(request, "front/order_detail.html", {"order": order})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    customer, _ = Customer.objects.get_or_create(user=request.user, defaults={
        "first_name": request.user.first_name or request.user.username,
        "email": request.user.email or "",
    })
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour")
            return redirect("front:profile")
    else:
        form = CustomerProfileForm(instance=customer)
    orders = customer.orders.select_related("customer").all()
    appointments = customer.appointments.select_related("service", "provider").all()
    return render(request, "front/profile.html", {"form": form, "orders": orders, "appointments": appointments})
