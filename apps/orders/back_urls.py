from __future__ import annotations

from django.urls import path

from . import back_views

urlpatterns = [
    path("", back_views.OrderListView.as_view(), name="list"),
    path("<int:pk>/", back_views.OrderDetailView.as_view(), name="detail"),
    path("<int:pk>/refund/", back_views.OrderRefundView.as_view(), name="refund"),
]
