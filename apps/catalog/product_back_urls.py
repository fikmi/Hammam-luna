from __future__ import annotations

from django.urls import path

from . import product_back_views

urlpatterns = [
    path("", product_back_views.ProductListView.as_view(), name="list"),
    path("new/", product_back_views.ProductCreateView.as_view(), name="create"),
    path("<int:pk>/", product_back_views.ProductUpdateView.as_view(), name="update"),
]
