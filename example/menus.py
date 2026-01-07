from flex_menu import MenuItem

from mvp.menus import SiteNavigation

# Add Inner Layouts menu with all demo views
SiteNavigation.append(
    MenuItem(
        name="Inner Layouts",
        extra_context={"icon": "grid"},
        children=[
            MenuItem(
                name="No Sidebars",
                view_name="dashboard",
                extra_context={"icon": "house"},
            ),
            MenuItem(
                name="Layout Demo",
                view_name="layout_demo",
                extra_context={"icon": "sliders"},
            ),
            MenuItem(
                name="Primary Sidebar",
                view_name="demo_primary_sidebar",
                extra_context={"icon": "sidebar"},
            ),
            MenuItem(
                name="Secondary Sidebar",
                url="#",
                extra_context={"icon": "sidebar"},
            ),
            MenuItem(
                name="Both",
                view_name="#",
                extra_context={"icon": "navbar"},
            ),
        ],
    ),
)

SiteNavigation.append(
    MenuItem(
        name="Examples",
        extra_context={"icon": "grid-3x3-gap"},
        children=[
            MenuItem(
                name="Products",
                view_name="product_list",
                extra_context={"icon": "box-seam"},
            ),
            MenuItem(
                name="Categories",
                view_name="category_list",
                extra_context={"icon": "folder"},
            ),
            MenuItem(
                name="Articles",
                view_name="article_list",
                extra_context={"icon": "newspaper"},
            ),
            MenuItem(
                name="Tasks",
                view_name="task_list",
                extra_context={"icon": "check2-square"},
            ),
        ],
    ),
)
