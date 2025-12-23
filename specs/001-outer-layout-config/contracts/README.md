# Contracts

This feature defines the shape of `PAGE_CONFIG` as consumed by templates and Cotton components.

- page_config.schema.json: JSON Schema describing the configuration object (`brand`, `sidebar`, `navbar`, `actions`).

Notes:
- The schema allows additional properties for forward compatibility.
- When `sidebar.show_at` is a breakpoint, `navbar.menu_visible_at` is ignored.
- The schema is for documentation; runtime validation is handled by the context processor.
