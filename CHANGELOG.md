# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Outer Layout Configuration System** (`PAGE_CONFIG`): Centralized configuration-driven layout system with per-region settings for sidebar, navbar, brand, and actions
  - **Per-region configuration**: `sidebar.*`, `navbar.*`, `brand`, `actions` keys (no top-level `navigation.*`)
  - **Smart defaults**: Navbar-only mode by default (`sidebar.show_at=False`, `menu_visible_at="sm"`)
  - **Single-source navigation**: Primary navigation renders in one region only (sidebar when in-flow, navbar otherwise) - prevents duplication
  - **Actions placement**: Actions automatically render in the active navigation region based on viewport and configuration
  - **Brand fallback**: Automatic fallback to text when theme-appropriate images are missing
  - **Breakpoint validation**: Validates Bootstrap 5 breakpoints (`sm`, `md`, `lg`, `xl`, `xxl`) with warning logs for invalid values
  - **Context processor integration**: `mvp.context_processors.page_config` exposes validated configuration to all templates
  - **Dynamic attr passthrough**: Uses Cotton's `:attrs` syntax for clean configuration flow to components
- Comprehensive test suite for layout configuration system covering navigation placement, brand/actions, responsive behavior, and edge cases
- Updated documentation in `docs/LAYOUT_CONFIGURATION.md` with complete schema reference, examples, and migration guide
- Example templates demonstrating configuration flow with explanatory comments

### Changed
- Context processor now enforces navbar-only mode by default (breaking change from previous implicit sidebar mode)
- Configuration validation now enforces single-source navigation rule: `navbar.menu_visible_at` is automatically ignored when `sidebar.show_at` is a breakpoint
- Brand and actions rendering now conditional based on configuration state rather than always present

### Fixed
- Eliminated duplicate navigation rendering when both sidebar and navbar were visible
- Proper responsive behavior for actions widgets (follow active navigation region)
- Brand image fallback now properly preserves accessibility

### Technical Details
- **Constitution Gates Validated**:
  - ✅ Gate A: No duplicate navigation (single-source rendering enforced)
  - ✅ Gate B: Framework-independent layout (works without Bootstrap)
  - ✅ Gate C: Template-only inner layout (no code dependencies)
  - ✅ Gate D: Accessibility (ARIA landmarks, focus order, keyboard navigation)
  - ✅ Gate E: Theming (Sass/CSS variables for customization)
  - ✅ Gate F: Progressive enhancement (JS optional, core functional without)
- **JSON Schema**: Complete configuration contract in `specs/001-outer-layout-config/contracts/page_config.schema.json`
- **Files Modified**:
  - `mvp/context_processors.py`: Added validation, defaults, enforcement rules
  - `mvp/templates/cotton/structure/sidebar/index.html`: Conditional actions rendering
  - `mvp/templates/cotton/structure/navbar/index.html`: Conditional actions rendering
  - `mvp/templates/cotton/structure/sidebar/widgets.html`: Actions visibility parameter
  - `tests/settings.py`: Updated example configuration
  - `tests/test_outer_layout_config.py`: New comprehensive test suite
  - `docs/LAYOUT_CONFIGURATION.md`: Complete rewrite for new system
  - `example/templates/layouts/base.html`: Added configuration flow comments

### Migration Notes
If upgrading from earlier versions:
1. Remove any `layout` key from `PAGE_CONFIG` (no longer used)
2. Set `sidebar.show_at=False` for navbar-only mode (new default)
3. Set `sidebar.show_at="lg"` (or preferred breakpoint) for sidebar mode
4. Add `navbar.menu_visible_at="sm"` for navbar-only mode
5. Ensure `actions` is a list at top level (not nested under navigation)
6. Review configuration schema in documentation for all available keys

### Added
- Initial project structure
- Basic app configuration
- Test suite setup
- CI/CD workflows

## [0.1.0] - 2025-12-09

### Added
- Initial alpha release
- Project scaffolding
- Poetry configuration
- GitHub Actions workflows
- Issue templates
- Copilot instructions

[Unreleased]: https://github.com/SamuelJennings/django-cotton-layouts/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SamuelJennings/django-cotton-layouts/releases/tag/v0.1.0
