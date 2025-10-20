from __future__ import annotations

from django.urls import path

from . import back_views

urlpatterns = [
    path("", back_views.ServiceListView.as_view(), name="list"),
    path("new/", back_views.ServiceCreateView.as_view(), name="create"),
    path("<int:pk>/", back_views.ServiceUpdateView.as_view(), name="update"),
]
