# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Layout Configuration System**: Complete support for AdminLTE 4 fixed positioning via `<c-app>` component attributes
  - **Fixed Sidebar** (`fixed_sidebar`): Makes sidebar sticky during vertical scrolling - ideal for admin dashboards
  - **Fixed Header** (`fixed_header`): Keeps top navigation bar fixed at the top - ideal for important navigation
  - **Fixed Footer** (`fixed_footer`): Keeps footer visible at the bottom - ideal for copyright notices or action buttons
  - **Combined Fixed Layouts**: All three attributes can be used simultaneously for complete fixed layout
  - **Responsive Sidebar Control** (`sidebar_expand`): Control sidebar expansion breakpoint (sm, md, lg, xl, xxl)
  - **Per-Page Layout Override**: Different pages can use different layout configurations
  - **Interactive Layout Demo Page**: Single unified demo page at `/layout/` for testing all layout configurations
    - Query parameter-based state management (bookmarkable URLs)
    - Split layout: main content area (col-lg-8) + configuration sidebar (col-lg-4)
    - Form controls for toggling fixed properties and responsive breakpoints
    - Real-time layout updates via GET requests
    - Visual indicators showing active CSS classes and configuration state
    - Extensible design allowing other features to add configuration options
  - CSS Classes: `.layout-fixed`, `.fixed-header`, `.fixed-footer`, `.sidebar-expand-{breakpoint}`
  - Component Documentation: [docs/components/app.md](docs/components/app.md)
  - Feature Specification: [specs/002-layout-configuration/](specs/002-layout-configuration/)
  - Test Coverage: 9 tests for unified demo page, plus component attribute tests

- **AdminLTE 4 Widget Components**: Complete implementation of three dashboard widget components
  - **Info Box Component** (`<c-info-box>`): Display metrics with icons and optional progress bars
    - Two fill modes: `fill="icon"` (default, colors icon only) and `fill="box"` (colors entire box)
    - Progress bar support using `<c-progress>` component with ARIA attributes
    - Bootstrap 5 color variants (primary, success, warning, danger, info, secondary)
    - Custom CSS class passthrough
    - Full accessibility support with proper ARIA attributes
    - Documentation: [docs/components/info-box.md](docs/components/info-box.md)
  - **Small Box Component** (`<c-small-box>`): Prominent dashboard summary widgets
    - Large metric display with colored background
    - Decorative background icons
    - Optional footer with action links (default text: "More info")
    - Custom link icon support
    - Bootstrap 5 color variants via `variant` attribute
    - Documentation: [docs/components/small-box.md](docs/components/small-box.md)
  - **Card Component** (`<c-card>`): Flexible content containers with collapsible sections
    - Three fill modes: `fill="outline"` (default, border only), `fill="header"` (header colored), `fill="card"` (entire card colored)
    - Optional icon in header
    - Named slots for `tools` and `footer`
    - AdminLTE card tools integration (collapse, maximize, remove buttons)
    - Collapsible state support via `collapsed` attribute
    - Documentation: [docs/components/card.md](docs/components/card.md)
- Comprehensive test suite with 30 tests covering all widget components (97% passing, 1 known Cotton limitation)
- Component documentation with complete API references, examples, and accessibility guidelines
- Documentation index at [docs/index.md](docs/index.md) with architecture overview and usage patterns

### Changed

- Updated README.md with accurate component examples matching actual implementations
- Component examples now use correct attribute names and values (`variant`, `fill`, etc.)

### Technical Details

- **Components Location**: `mvp/templates/cotton/`
- **Test Coverage**: 29/30 tests passing (info-box: 8/8, small-box: 9/9, card: 12/13)
- **Known Limitation**: One card test fails due to Cotton `_children` behavior (documented)
- **Dependencies**: Requires `django-cotton`, `django-cotton-bs5`, `django-easy-icons`
- **Accessibility**: All components follow WCAG 2.1 AA guidelines with proper ARIA attributes
- **Files Added**:
  - `mvp/templates/cotton/info_box.html`
  - `mvp/templates/cotton/small_box.html`
  - `mvp/templates/cotton/card.html`
  - `tests/test_info_box.py` (8 tests)
  - `tests/test_small_box.py` (9 tests)
  - `tests/test_card.py` (13 tests)
  - `docs/components/info-box.md`
  - `docs/components/small-box.md`
  - `docs/components/card.md`
  - `docs/index.md`
- **Specification**: `specs/003-default-widgets/`

---

- **Outer Layout Configuration System** (`PAGE_CONFIG`): Centralized configuration-driven layout system with per-region settings for sidebar, navbar, brand, and actions
  - **Per-region configuration**: `sidebar.*`, `navbar.*`, `brand`, `actions` keys (no top-level `navigation.*`)
  - **Smart defaults**: Navbar-only mode by default (`sidebar.show_at=False`, `breakpoint="sm"`)
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
- Configuration validation now enforces single-source navigation rule: `navbar.breakpoint` is automatically ignored when `sidebar.show_at` is a breakpoint
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
4. Add `navbar.breakpoint="sm"` for navbar-only mode
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
