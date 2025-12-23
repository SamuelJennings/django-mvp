"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path

from .views import (
    ArticleDetailView,
    ArticleListView,
    CategoryDetailView,
    CategoryListView,
    HomeView,
    ProductDetailView,
    ProductListView,
    TaskDetailView,
    TaskListView,
    ThemeTestView,
)

urlpatterns = [
    # Home page with layout demo
    path("", HomeView.as_view(), name="index"),
    path("demo/theme-test/", ThemeTestView.as_view(), name="theme_test"),
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
