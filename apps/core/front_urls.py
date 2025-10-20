from __future__ import annotations

from django.urls import path

from . import front_views

urlpatterns = [
    path("", front_views.home, name="home"),
    path("services/", front_views.service_list, name="services"),
    path("services/<int:pk>/", front_views.service_detail, name="service_detail"),
    path("services/<int:service_id>/book/", front_views.appointment_booking, name="appointment_book"),
    path("appointments/<int:appointment_id>/confirm/", front_views.appointment_confirm, name="appointment_confirm"),
    path("products/", front_views.product_list, name="products"),
    path("products/<int:pk>/", front_views.product_detail, name="product_detail"),
    path("cart/", front_views.cart_view, name="cart"),
    path("cart/add/service/<int:service_id>/", front_views.cart_add_service, name="cart_add_service"),
    path("cart/add/product/<int:product_id>/", front_views.cart_add_product, name="cart_add_product"),
    path("cart/remove/<str:item_id>/", front_views.cart_remove, name="cart_remove"),
    path("checkout/", front_views.checkout, name="checkout"),
    path("orders/<int:order_id>/", front_views.order_detail, name="order_detail"),
    path("profil/", front_views.profile, name="profile"),
]
