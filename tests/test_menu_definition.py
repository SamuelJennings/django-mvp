"""Tests for menu definition API (MenuItem and AppMenu).

Tests cover:
- Empty AppMenu initialization
- MenuItem creation with view_name and extra_context
- Adding MenuItem instances to AppMenu.children
"""


class TestEmptyAppMenu:
    """Test empty AppMenu renders without items (US3)."""

    def test_empty_app_menu_has_no_children(self, app_menu):
        """T008: Empty AppMenu should initialize with no children."""
        assert len(app_menu.children) == 0
        assert app_menu.name == "AppMenu"

    def test_empty_app_menu_can_be_imported(self):
        """T008: AppMenu should be importable from mvp.menus."""
        from mvp.menus import AppMenu

        assert AppMenu is not None
        assert AppMenu.name == "AppMenu"


class TestMenuItemCreation:
    """Test MenuItem creation with Python API (US4)."""

    def test_menuitem_with_name_and_view_name(self, menu_item_factory):
        """T010: Create MenuItem with name and view_name."""
        item = menu_item_factory(name="home", view_name="app:home")

        assert item.name == "home"
        assert item.view_name == "app:home"

    def test_menuitem_with_extra_context(self, menu_item_factory):
        """T011: Create MenuItem with extra_context (label, icon)."""
        item = menu_item_factory(
            name="dashboard",
            view_name="app:dashboard",
            extra_context={"label": "Dashboard", "icon": "speedometer"},
        )

        assert item.extra_context["label"] == "Dashboard"
        assert item.extra_context["icon"] == "speedometer"

    def test_menuitem_with_minimal_params(self, menu_item_factory):
        """T011: MenuItem can be created with minimal parameters."""
        item = menu_item_factory(name="test")

        assert item.name == "test"
        assert item.view_name is None
        assert item.extra_context == {}


class TestAddingItemsToAppMenu:
    """Test adding MenuItem to AppMenu.children (US4)."""

    def test_add_single_item_to_app_menu(self, app_menu, menu_item_factory):
        """T012: Add MenuItem to AppMenu by setting parent."""
        item = menu_item_factory(name="home", view_name="app:home")
        item.parent = app_menu

        assert len(app_menu.children) == 1
        assert app_menu.children[0].name == "home"

    def test_add_multiple_items_to_app_menu(self, app_menu):
        """T012: Add multiple MenuItems to AppMenu using parent parameter."""
        from flex_menu import MenuItem

        MenuItem(name="home", view_name="app:home", parent=app_menu)
        MenuItem(name="about", view_name="app:about", parent=app_menu)

        assert len(app_menu.children) == 2
        assert app_menu.children[0].name == "home"
        assert app_menu.children[1].name == "about"

    def test_app_menu_children_preserves_order(self, app_menu):
        """T012: AppMenu.children should preserve declaration order."""
        from flex_menu import MenuItem

        for i in range(5):
            MenuItem(name=f"item{i}", parent=app_menu)

        assert len(app_menu.children) == 5
        for i, item in enumerate(app_menu.children):
            assert item.name == f"item{i}"
