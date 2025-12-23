# Implementation Plan: Outer Layout Configuration System

**Branch**: `001-outer-layout-config` | **Date**: 2025-12-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-outer-layout-config/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a configuration-driven outer layout system where a single `PAGE_CONFIG` dictionary in Django settings controls navigation placement, branding, actions, and responsive behavior. The layout templates consume config partials via Cotton's dynamic `:attrs` syntax, eliminating per-template duplication and ensuring single-source navigation rendering per constitution Principle III. Default values provide a working navbar-only layout out of the box.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Django 4.2+, django-cotton, django-cotton-bs5, django-flex-menus, django-easy-icons, django-compressor, django-libsass  
**Storage**: N/A (configuration-only feature)  
**Testing**: pytest with Django test client; template rendering unit tests  
**Target Platform**: Django server-side rendering (SSR) with optional TypeScript-compiled client behaviors  
**Project Type**: Django app (web)  
**Performance Goals**: Template rendering <50ms; compiled assets cacheable; no runtime bundler  
**Constraints**: Framework-independent layout CSS; no duplicate navigation; template-only inner layout; accessible and responsive  
**Scale/Scope**: Core package feature affecting all layouts; ~5-10 test cases for config variations, navigation placement, responsiveness

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gate A**: No duplicate navigation across navbar/sidebar for selected mode. ✅ PASS (FR-002, FR-009 enforce single-source nav; context processor logic validates mode)
- **Gate B**: Layout renders without any CSS framework present. ✅ PASS (FR-008 mandates framework-independent layout CSS; namespaced)
- **Gate C**: Inner layout regions reflect template attributes only; no alternate configuration path exists; no duplication or conflict is present. ✅ PASS (Out of scope for this feature; constitution Principle IV already enforced)
- **Gate D**: Basic accessibility landmarks and ARIA focus order present. ✅ PASS (FR-012 requires accessibility tests; components use semantic HTML and ARIA)
- **Gate E**: Theming works via both Sass (build-time) and CSS variables (runtime) in sample pages. ✅ PASS (Existing theme system supports both; not modified by this feature)
- **Gate F**: Compiled JS assets are present and functional without any external bundler; core layout remains usable with JS disabled. ✅ PASS (Optional TypeScript behaviors precompiled; progressive enhancement per constitution Principle IX)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
mvp/
├── context_processors.py         # page_config exposure and validation
├── templates/
│   ├── base.html                 # Foundation HTML, loads assets
│   ├── layouts/
│   │   ├── base.html             # Minimal extension of base.html
│   │   └── standard.html         # Outer layout consuming page_config via :attrs
│   └── cotton/
│       └── page/
│           ├── navigation/
│           │   ├── sidebar.html  # Sidebar component accepting :attrs
│           │   └── navbar.html   # Navbar component accepting :attrs
│           └── brand.html        # Brand component for both regions
└── static/
    └── scss/
        └── _layout.scss          # Framework-independent layout CSS

tests/
├── settings.py                   # Example PAGE_CONFIG
├── test_layout_config.py         # Config validation, navigation placement, brand/actions
└── test_app.py                   # General app tests (existing)

example/
└── templates/
    └── example/
        └── *.html                # Demo pages extending layouts/standard.html
```

**Structure Decision**: Django app structure. Core logic in `mvp/context_processors.py` validates and exposes `PAGE_CONFIG`. Templates in `mvp/templates/` consume config via Cotton's `:attrs`. Tests verify navigation placement, responsiveness, and absence of duplication per functional requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All gates pass.
