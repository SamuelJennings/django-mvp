# Data Model: PAGE_CONFIG

This document defines the configuration shape injected into templates via the
context processor `mvp.context_processors.page_config`.

## Top-level keys

- brand: Brand
- sidebar: SidebarOptions
- navbar: NavbarOptions
- actions: Action[]

## Brand
- text: string
- image_light?: string (static path)
- image_dark?: string (static path)
- icon_light?: string (static path)
- icon_dark?: string (static path)

## SidebarOptions
- show_at: false | null | "sm" | "md" | "lg" | "xl" | "xxl"
- collapsible?: boolean (default: true)
- width?: string (default: "260px")

## NavbarOptions
- fixed?: boolean (default: false)
- border?: boolean (default: false)
- menu_visible_at?: false | null | "sm" | "md" | "lg" | "xl" | "xxl" (default: "lg")

Notes:
- When `sidebar.show_at` is a breakpoint, `navbar.menu_visible_at` is ignored.
- When `sidebar.show_at` is false/null, navbar-only mode applies and
  `navbar.menu_visible_at` determines when the menu appears.

## Action
- icon: string (easy-icons name)
- text: string
- href: string (URL)
- target?: string (e.g., "_blank")
- id?: string
