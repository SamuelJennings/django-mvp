"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="example/dashboard.html"), name="dashboard"),
    path("layout-fixed/", views.layout_fixed_demo, name="layout_fixed_demo"),
    path("layout-responsive/", views.layout_responsive_demo, name="layout_responsive_demo"),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
