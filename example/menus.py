from flex_menu import MenuItem

from cotton_layouts.menus import SiteNavigation

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
