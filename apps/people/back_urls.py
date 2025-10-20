from __future__ import annotations

from django.urls import path

from . import back_views

urlpatterns = [
    path("", back_views.ProviderListView.as_view(), name="list"),
    path("new/", back_views.ProviderCreateView.as_view(), name="create"),
    path("<int:pk>/", back_views.ProviderUpdateView.as_view(), name="update"),
]
