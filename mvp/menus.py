from flex_menu import Menu, MenuItem

SiteNavigation = Menu(
    "Site Navigation",
    children=[
        MenuItem(
            name="Home",
            view_name="index",
            extra_context={"icon": "house"},
        ),
    ],
)
