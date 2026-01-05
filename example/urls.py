"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path

from .views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
