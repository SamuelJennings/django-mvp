"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path

from .views import (
    ArticleDetailView,
    ArticleListView,
    CategoryDetailView,
    CategoryListView,
    DemoBothLayoutView,
    DemoDualSidebarView,
    DemoLayoutSwitcherView,
    DemoNavbarOnlyView,
    DemoSidebarLeftView,
    DemoSidebarOnlyView,
    DemoSidebarRightView,
    DemoSingleColumnView,
    LayoutDemoView,
    ProductDetailView,
    ProductListView,
    TaskDetailView,
    TaskListView,
    ThemeTestView,
)

urlpatterns = [
    # Layout demos
    path("", LayoutDemoView.as_view(), name="index"),
    path("demo/", LayoutDemoView.as_view(), name="layout_demo"),
    path("demo/theme-test/", ThemeTestView.as_view(), name="theme_test"),
    # New layout demos
    path("demo/navbar-only/", DemoNavbarOnlyView.as_view(), name="demo_navbar_only"),
    path("demo/sidebar-only/", DemoSidebarOnlyView.as_view(), name="demo_sidebar_only"),
    path("demo/both-layout/", DemoBothLayoutView.as_view(), name="demo_both_layout"),
    path("demo/layout-switcher/", DemoLayoutSwitcherView.as_view(), name="demo_layout_switcher"),
    path("demo/single-column/", DemoSingleColumnView.as_view(), name="demo_single_column"),
    path("demo/sidebar-left/", DemoSidebarLeftView.as_view(), name="demo_sidebar_left"),
    path("demo/sidebar-right/", DemoSidebarRightView.as_view(), name="demo_sidebar_right"),
    path("demo/dual-sidebar/", DemoDualSidebarView.as_view(), name="demo_dual_sidebar"),
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
