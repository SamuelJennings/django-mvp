"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView

from .views import (
    ArticleDetailView,
    ArticleListView,
    CategoryDetailView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
    TaskDetailView,
    TaskListView,
)

urlpatterns = [
    # Home page with layout demo
    path("", TemplateView.as_view(template_name="demo/home.html"), name="index"),
    path("demo/theme-test/", TemplateView.as_view(template_name="demo/theme_test.html"), name="theme_test"),
    # Inner layout demos
    path(
        "demo/primary-sidebar/",
        TemplateView.as_view(template_name="demo/demo_primary_sidebar.html"),
        name="demo_primary_sidebar",
    ),
    path(
        "demo/secondary-sidebar/",
        TemplateView.as_view(template_name="demo/demo_secondary_sidebar.html"),
        name="demo_secondary_sidebar",
    ),
    path(
        "demo/dual-sidebars/",
        TemplateView.as_view(template_name="demo/demo_dual_sidebars.html"),
        name="demo_dual_sidebars",
    ),
    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    # Categories
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"),
    # Articles
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    # Tasks
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
