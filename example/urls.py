"""Example app URL configuration."""

from django.conf import settings
from django.urls import include, path

from . import views
from .views import BasicListViewDemo, ListViewDemo, MinimalListViewDemo, MVPDemoView

urlpatterns = [
    # Main dashboard
    path("", MVPDemoView.as_view(template_name="example/dashboard.html"), name="dashboard"),
    path("layout/", views.LayoutDemoView.as_view(), name="layout_demo"),
    path("page-layout/", views.PageLayoutDemoView.as_view(), name="page_layout_demo"),
    path("widgets/", views.NavbarWidgetsView.as_view(), name="navbar_widgets_demo"),
    path("list-view/", ListViewDemo.as_view(), name="list_view_demo"),
    path("list-view/minimal/", MinimalListViewDemo.as_view(), name="minimal_list_demo"),
    path("list-view/basic/", BasicListViewDemo.as_view(), name="basic_list_demo"),
    # Grid configuration demos (T015-T018) - same view, different grid parameters
    path("list-view/grid/1col/", MinimalListViewDemo.as_view(grid={"cols": 1}), name="grid_demo_1col"),
    path("list-view/grid/2col/", MinimalListViewDemo.as_view(grid={"cols": 1, "md": 2}), name="grid_demo_2col"),
    path(
        "list-view/grid/3col/", MinimalListViewDemo.as_view(grid={"cols": 1, "md": 2, "lg": 3}), name="grid_demo_3col"
    ),
    path(
        "list-view/grid/responsive/",
        MinimalListViewDemo.as_view(grid={"cols": 1, "sm": 2, "md": 3, "xl": 4, "gap": 3}),
        name="grid_demo_responsive",
    ),
    path("form-view/", views.FormViewDemo.as_view(), name="form_view_demo"),
    # ===================== FAKE URLS TO TEST MENU SIDEBAR BEHAVIOR ======================================
    path("profile/", MVPDemoView.as_view(template_name="example/profile.html"), name="profile"),
    path("admin/users/", MVPDemoView.as_view(template_name="example/admin/users.html"), name="admin_users"),
    path(
        "admin/permissions/",
        MVPDemoView.as_view(template_name="example/admin/permissions.html"),
        name="admin_permissions",
    ),
    path("admin/settings/", MVPDemoView.as_view(template_name="example/admin/settings.html"), name="admin_settings"),
    path(
        "content/articles/",
        MVPDemoView.as_view(template_name="example/content/articles.html"),
        name="content_articles",
    ),
    path("content/pages/", MVPDemoView.as_view(template_name="example/content/pages.html"), name="content_pages"),
    path("content/media/", MVPDemoView.as_view(template_name="example/content/media.html"), name="content_media"),
    path(
        "tools/import-export/",
        MVPDemoView.as_view(template_name="example/tools/import_export.html"),
        name="tools_import_export",
    ),
    path("tools/backup/", MVPDemoView.as_view(template_name="example/tools/backup.html"), name="tools_backup"),
    path("tools/logs/", MVPDemoView.as_view(template_name="example/tools/logs.html"), name="tools_logs"),
    path(
        "reports/users/active/",
        MVPDemoView.as_view(template_name="example/reports/active_users.html"),
        name="reports_active_users",
    ),
    path(
        "reports/users/activity/",
        MVPDemoView.as_view(template_name="example/reports/user_activity.html"),
        name="reports_user_activity",
    ),
    path(
        "reports/content/",
        MVPDemoView.as_view(template_name="example/reports/content_stats.html"),
        name="reports_content_stats",
    ),
    path(
        "reports/system/",
        MVPDemoView.as_view(template_name="example/reports/system_health.html"),
        name="reports_system_health",
    ),
    # API documentation
    path("api/docs/", MVPDemoView.as_view(template_name="example/api/docs.html"), name="api_docs"),
    # =============================================================================
    # TESTING URLS FOR INTEGRATION TESTS
    # =============================================================================
    # These support the integration test scenarios
    path("test1/", MVPDemoView.as_view(template_name="example/test1.html"), name="test1"),
    path("test2/", MVPDemoView.as_view(template_name="example/test2.html"), name="test2"),
    path("mvp/", MVPDemoView.as_view(template_name="example/mvp.html"), name="mvp_item"),
    path("example/", MVPDemoView.as_view(template_name="example/example.html"), name="example_item"),
    path("third/", MVPDemoView.as_view(template_name="example/third.html"), name="third_app_item"),
    path("valid/", MVPDemoView.as_view(template_name="example/valid.html"), name="valid_item"),
    path("direct/", MVPDemoView.as_view(template_name="example/direct.html"), name="direct_url"),
    path("external/", MVPDemoView.as_view(template_name="example/external.html"), name="external_url"),
    path("notifications/", MVPDemoView.as_view(template_name="example/notifications.html"), name="notifications"),
    path("messages/", MVPDemoView.as_view(template_name="example/messages.html"), name="messages"),
    path("settings/", MVPDemoView.as_view(template_name="example/settings.html"), name="settings"),
    # Parameterized URL for testing
    path(
        "users/<int:user_id>/profile/",
        MVPDemoView.as_view(template_name="example/user_profile.html"),
        name="user_profile",
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
