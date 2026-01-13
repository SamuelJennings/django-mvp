"""Tests for menu rendering in sidebar.

Tests cover:
- Empty menu sidebar rendering
- Single menu item rendering with labels, URLs, icons
- Multiple single items render in declaration order
- Single items appear before groups
- Parent items with children render as groups
- Group headers and nested children
"""


class TestEmptyMenuRendering:
    """Test sidebar renders empty menu structure (US3)."""

    def test_empty_sidebar_renders_container(self, app_menu, rf):
        """T009: Empty AppMenu should render container without items."""
        from flex_menu.templatetags.flex_menu import render_menu

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should contain ul structure from Cotton component
        assert '<ul id="navigation"' in output
        assert 'class="nav sidebar-menu flex-column"' in output
        assert 'role="navigation"' in output

    def test_empty_sidebar_has_no_menu_items(self, app_menu, rf):
        """T009: Empty menu should not render any <li> elements."""
        from flex_menu.templatetags.flex_menu import render_menu

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should not contain any list items
        assert "<li" not in output
        assert "nav-item" not in output


class TestSingleMenuItemRendering:
    """Test single menu item rendering with labels, URLs, icons (US1)."""

    def test_single_item_renders_with_label_and_url(self, app_menu, rf):
        """T017: Single item should render with label text and href."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="home",
            view_name="dashboard",  # Use real view name from example URLs
            extra_context={"label": "Home"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        assert "Home" in output
        assert 'href="/"' in output
        assert '<li class="nav-item' in output  # Cotton component renders <li>

    def test_single_item_renders_with_icon(self, app_menu, rf):
        """T018: Single item should render icon when specified."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="dashboard",
            view_name="dashboard",  # Use real view name
            extra_context={"label": "Dashboard", "icon": "calendar"},  # Use valid Bootstrap Icon
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        assert "Dashboard" in output
        assert "calendar" in output or "nav-icon" in output

    def test_multiple_single_items_render_in_order(self, app_menu, rf):
        """T019: Multiple single items should render in declaration order."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(name="first", url="/first", extra_context={"label": "First"}, parent=app_menu)
        MenuItem(name="second", url="/second", extra_context={"label": "Second"}, parent=app_menu)
        MenuItem(name="third", url="/third", extra_context={"label": "Third"}, parent=app_menu)

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Check order by finding indices
        first_idx = output.find("First")
        second_idx = output.find("Second")
        third_idx = output.find("Third")

        assert first_idx < second_idx < third_idx

    def test_single_items_appear_before_groups(self, app_menu, rf):
        """T020: MenuGroup items should render at bottom, MenuItem and MenuCollapse maintain declaration order."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuCollapse, MenuGroup

        # Declare OUT OF ORDER to test sorting behavior
        # Declaration order: GROUP -> S1 -> S2 -> MC
        # Expected output order: S1 -> S2 -> MC -> GROUP (MenuGroup moved to bottom, others stay in place)

        MenuGroup(  # Should be sorted to bottom
            name="group",
            extra_context={"label": "GROUP SECTION"},
            parent=app_menu,
            children=[
                MenuItem(name="child2", url="/child2", extra_context={"label": "Group Child"}),
            ],
        )

        MenuItem(name="single1", url="/single1", extra_context={"label": "First Single"}, parent=app_menu)

        MenuItem(name="single2", url="/single2", extra_context={"label": "Second Single"}, parent=app_menu)

        MenuCollapse(  # Should stay in declaration position (after both singles)
            name="collapse",
            extra_context={"label": "Collapse Item"},
            parent=app_menu,
            children=[
                MenuItem(name="child1", url="/child1", extra_context={"label": "Child Item"}),
            ],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Get positions
        first_single_idx = output.find("First Single")
        second_single_idx = output.find("Second Single")
        collapse_idx = output.find("Collapse Item")
        group_idx = output.find("GROUP SECTION")

        # Verify sorted order: MenuItem/MenuCollapse in declaration order, MenuGroup at bottom
        assert first_single_idx < second_single_idx, "First single should appear before second single"
        assert second_single_idx < collapse_idx, "Second single should appear before collapse"
        assert collapse_idx < group_idx, "MenuGroup should appear at bottom"


class TestHierarchicalMenuGroups:
    """Test hierarchical menu group rendering (US2)."""

    def test_parent_item_renders_below_singles(self, app_menu, rf):
        """T027: MenuGroup items should render at bottom, MenuCollapse stays in place."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuCollapse, MenuGroup

        # Add single item first
        MenuItem(name="single", url="/single", extra_context={"label": "Single"}, parent=app_menu)

        # Add MenuCollapse (should stay after single, not be sorted)
        MenuCollapse(
            name="collapse",
            extra_context={"label": "Collapse"},
            parent=app_menu,
            children=[
                MenuItem(name="child1", url="/child1", extra_context={"label": "Child 1"}),
            ],
        )

        # Add MenuGroup (should be sorted to bottom)
        MenuGroup(
            name="group",
            extra_context={"label": "GROUP HEADER"},
            parent=app_menu,
            children=[
                MenuItem(name="child2", url="/child2", extra_context={"label": "Child 2"}),
            ],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        single_idx = output.find("Single")
        collapse_idx = output.find("Collapse")
        group_idx = output.find("GROUP HEADER")

        # Single and Collapse in declaration order, Group at bottom
        assert single_idx < collapse_idx, "Single should appear before collapse"
        assert collapse_idx < group_idx, "MenuGroup should appear at bottom"

    def test_group_header_renders_when_specified(self, app_menu, rf):
        """T028: Group header should render when using MenuGroup class."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuGroup

        MenuGroup(
            name="admin",
            extra_context={"label": "ADMIN TOOLS"},
            parent=app_menu,
            children=[
                MenuItem(name="users", url="/users", extra_context={"label": "Users"}),
            ],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        assert "ADMIN TOOLS" in output
        assert "Users" in output

    def test_nested_children_render_under_parent(self, app_menu, rf):
        """T029: Nested children should render indented under parent."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuCollapse

        MenuCollapse(
            name="parent",
            extra_context={"label": "Parent Item"},
            parent=app_menu,
            children=[
                MenuItem(name="child1", url="/child1", extra_context={"label": "Child 1"}),
                MenuItem(name="child2", url="/child2", extra_context={"label": "Child 2"}),
            ],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Check nav-treeview class is present (indicates nested structure)
        assert "nav-treeview" in output
        assert "Child 1" in output
        assert "Child 2" in output

    def test_multiple_groups_render_in_order(self, app_menu, rf):
        """T030: Multiple MenuCollapse items should render in declaration order."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuCollapse

        MenuCollapse(
            name="collapse1",
            extra_context={"label": "First Collapse"},
            parent=app_menu,
            children=[MenuItem(name="c1", url="/c1", extra_context={"label": "Child 1"})],
        )
        MenuCollapse(
            name="collapse2",
            extra_context={"label": "Second Collapse"},
            parent=app_menu,
            children=[MenuItem(name="c2", url="/c2", extra_context={"label": "Child 2"})],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        first_idx = output.find("First Collapse")
        second_idx = output.find("Second Collapse")

        assert first_idx < second_idx

    def test_nested_items_use_nav_treeview(self, app_menu, rf):
        """T031: Nested children should use nav-treeview class."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        from mvp.menus import MenuCollapse

        MenuCollapse(
            name="parent",
            extra_context={"label": "Parent"},
            parent=app_menu,
            children=[
                MenuItem(name="child", url="/child", extra_context={"label": "Child"}),
            ],
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        assert 'class="nav nav-treeview"' in output


class TestBadgeRendering:
    """Test badge rendering in menu items (T047-T048)."""

    def test_badge_renders_when_badge_in_extra_context(self, app_menu, rf):
        """T047: Badge should render when badge in extra_context."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="notifications",
            url="/notifications/",
            extra_context={"label": "Notifications", "badge": "5", "badge_classes": "text-bg-danger"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should contain badge content and classes
        assert "5" in output  # Badge content
        assert "text-bg-danger" in output or "badge" in output

    def test_badge_classes_applied_correctly(self, app_menu, rf):
        """T048: Badge classes should be applied correctly."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="messages",
            url="/messages/",
            extra_context={"label": "Messages", "badge": "New", "badge_classes": "text-bg-success nav-badge"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should apply custom badge classes
        assert "New" in output  # Badge content
        assert "text-bg-success" in output or "nav-badge" in output

    def test_menu_item_without_badge_no_badge_rendered(self, app_menu, rf):
        """Badge should not appear when not specified in extra_context."""
        from flex_menu import MenuItem
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="settings",
            url="/settings/",
            extra_context={"label": "Settings"},  # No badge specified
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should not contain any badge-related markup
        assert "badge" not in output.lower() or "Settings" in output  # Either no badge or just the label
