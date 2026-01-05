"""Example views for demonstrating AdminLTE layout."""

from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Simple dashboard view demonstrating AdminLTE layout."""

    template_name = "example/dashboard.html"
