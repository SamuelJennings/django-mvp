"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Main dashboard
    path("", TemplateView.as_view(template_name="example/dashboard.html"), name="dashboard"),
    # Layout demonstration
    path("layout/", views.layout_demo, name="layout_demo"),
    # Inner layout demonstration
    path("page-layout/", views.page_layout_demo, name="page_layout_demo"),
    # Navbar widgets demonstration
    path("widgets/", views.navbar_widgets_demo, name="navbar_widgets_demo"),
    # =============================================================================
    # MENU TESTING URLS
    # =============================================================================
    # These URLs support the comprehensive menu examples in menus.py
    # Profile section
    path("profile/", TemplateView.as_view(template_name="example/profile.html"), name="profile"),
    # Administration URLs
    path("admin/users/", TemplateView.as_view(template_name="example/admin/users.html"), name="admin_users"),
    path(
        "admin/permissions/",
        TemplateView.as_view(template_name="example/admin/permissions.html"),
        name="admin_permissions",
    ),
    path("admin/settings/", TemplateView.as_view(template_name="example/admin/settings.html"), name="admin_settings"),
    # Content management URLs
    path(
        "content/articles/",
        TemplateView.as_view(template_name="example/content/articles.html"),
        name="content_articles",
    ),
    path("content/pages/", TemplateView.as_view(template_name="example/content/pages.html"), name="content_pages"),
    path("content/media/", TemplateView.as_view(template_name="example/content/media.html"), name="content_media"),
    # Tools & utilities
    path(
        "tools/import-export/",
        TemplateView.as_view(template_name="example/tools/import_export.html"),
        name="tools_import_export",
    ),
    path("tools/backup/", TemplateView.as_view(template_name="example/tools/backup.html"), name="tools_backup"),
    path("tools/logs/", TemplateView.as_view(template_name="example/tools/logs.html"), name="tools_logs"),
    # Reports & analytics
    path(
        "reports/users/active/",
        TemplateView.as_view(template_name="example/reports/active_users.html"),
        name="reports_active_users",
    ),
    path(
        "reports/users/activity/",
        TemplateView.as_view(template_name="example/reports/user_activity.html"),
        name="reports_user_activity",
    ),
    path(
        "reports/content/",
        TemplateView.as_view(template_name="example/reports/content_stats.html"),
        name="reports_content_stats",
    ),
    path(
        "reports/system/",
        TemplateView.as_view(template_name="example/reports/system_health.html"),
        name="reports_system_health",
    ),
    # API documentation
    path("api/docs/", TemplateView.as_view(template_name="example/api/docs.html"), name="api_docs"),
    # =============================================================================
    # TESTING URLS FOR INTEGRATION TESTS
    # =============================================================================
    # These support the integration test scenarios
    path("test1/", TemplateView.as_view(template_name="example/test1.html"), name="test1"),
    path("test2/", TemplateView.as_view(template_name="example/test2.html"), name="test2"),
    path("mvp/", TemplateView.as_view(template_name="example/mvp.html"), name="mvp_item"),
    path("example/", TemplateView.as_view(template_name="example/example.html"), name="example_item"),
    path("third/", TemplateView.as_view(template_name="example/third.html"), name="third_app_item"),
    path("valid/", TemplateView.as_view(template_name="example/valid.html"), name="valid_item"),
    path("direct/", TemplateView.as_view(template_name="example/direct.html"), name="direct_url"),
    path("external/", TemplateView.as_view(template_name="example/external.html"), name="external_url"),
    path("notifications/", TemplateView.as_view(template_name="example/notifications.html"), name="notifications"),
    path("messages/", TemplateView.as_view(template_name="example/messages.html"), name="messages"),
    path("settings/", TemplateView.as_view(template_name="example/settings.html"), name="settings"),
    # Parameterized URL for testing
    path(
        "users/<int:user_id>/profile/",
        TemplateView.as_view(template_name="example/user_profile.html"),
        name="user_profile",
    ),
    # =============================================================================
    # INNER LAYOUT DEMO URLS
    # =============================================================================
    path(
        "page-layout/",
        TemplateView.as_view(template_name="example/page_layout.html"),
        name="page_layout_demo",
    ),
]

# Django Tables2 demo (optional dependency)
try:
    from example.views import DataTablesView

    urlpatterns.append(
        path("datatables-demo/", DataTablesView.as_view(), name="datatables_demo"),
    )
except ImportError:
    pass


if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
