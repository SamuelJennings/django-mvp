<!--
Sync Impact Report
- Version change: 3.0.0 → 3.1.0
- Modified principles:
	- Added IX. Client-Side Behavior (TypeScript, Precompiled)
- Added sections: Gate F under Development Workflow
- Removed sections: none
- Templates requiring updates:
	- .specify/templates/plan-template.md → ✅ aligns (Constitution Check gains Gate F)
	- .specify/templates/spec-template.md → ✅ aligns (no changes required)
	- .specify/templates/tasks-template.md → ✅ aligns (no changes required)
	- .specify/templates/commands/* → ⚠ pending (commands directory not present to verify)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): Original adoption date unknown; set when first ratified.
	- Optional: add a DEBUG-time validator that flags conflicting inner layout declarations.
-->

# django-mvp Constitution

## Core Principles

### I. Configuration-First Layout (NON-NEGOTIABLE)
The outer application layout MUST be driven by a single Django settings object
(the "page configuration"), not by per-template edits. A fresh install MUST
render a working site using sensible defaults without requiring user CSS or
utility classes for basic structure.

Rationale: Configuration over code enables reproducible, predictable behavior
and dramatically reduces the need for boilerplate templates.

### II. Framework-Independent Layout Engine
The core layout system (application shell, page regions, inner content shell)
MUST be independent of any CSS framework. The project SHALL ship its own
namespaced layout styles to control structure and responsiveness. Component
libraries MAY rely on a framework (e.g., Bootstrap 5) for look-and-feel, but
the layout engine MUST function without any framework CSS present.

Rationale: Decoupling structure from presentation enables pluggable component
libraries and consistent behavior across themes.

### III. Single-Source Navigation Rendering
Navigation MUST render in only one primary location at a time based on the
configured layout:
- Navbar-only: Navigation appears in the navbar; sidebar MUST NOT render nav.
- Sidebar-only: Navigation appears in the sidebar; navbar MUST NOT render nav.
- Sidebar + Navbar: Elements MUST NOT be duplicated; distribution MUST be
	explicit (e.g., primary nav in sidebar, utility/actions in navbar).

Rationale: Avoids duplicate navigation, reduces cognitive load, and ensures a
coherent IA across layouts.

### IV. Inner Layout via Templates (Template-Only)
Inner content layout (optional left/right sidebars and main content) MUST be
declared exclusively in the template via the inner-layout component’s
attributes. There are no view-mixin or global-settings controls for inner
layout.

Guardrails: The system MUST prevent contradictory or duplicate region
definitions. Under DEBUG, validation SHOULD flag conflicts to guide developers.

Rationale: Most users expect to adjust layout in templates. Template-only keeps
configuration discoverable and avoids drift between Python defaults and
templates.

### V. Component Library Abstraction
All outer layout slots (sidebar, navbar, toolbar, content panels) MUST render
through a component library contract. The default library targets Bootstrap 5.
A component library SHOULD expose subcomponents for common needs (e.g.,
sidebar.brand, sidebar.menu-group, sidebar.menu-item; toolbar.actions,
toolbar.inputs, toolbar.dropdown). Usage is optional, but the contract MUST be
stable so libraries can be swapped via configuration.

Rationale: Clear contracts enable themed or framework-specific component packs
without changing layout semantics.

### VI. Theming and Assets: Build-time and Runtime
The system MUST support both:
- Build-time theming via Sass variables and custom SCSS compiled with
	django-compressor + django-libsass.
- Runtime theming via CSS variables for dynamic adjustments without rebuilds.
Compiled assets MUST be cacheable and safe to regenerate.

Rationale: Teams can choose between precompiled themes and runtime tuning based
on deployment model.

### VII. Accessibility and Responsiveness
Layout and navigation MUST be fully responsive and accessible:
- Keyboard navigable and ARIA-annotated key landmarks/controls.
- Works without JavaScript for core navigation.
- Verified at common breakpoints (mobile, tablet, desktop).

Rationale: Inclusive design and reliable behavior across devices are
non-negotiable for production UX.

### VIII. Composable, Well-Maintained Dependencies
The project integrates well-tested packages (django-easy-icons,
django-flex-menus, django-cotton, django-compressor, django-libsass). These are
treated as composable building blocks. Upgrades MUST follow semantic versioning
and include smoke checks for layout integrity and navigation rules.

Rationale: Leverage mature ecosystem packages while maintaining stability.

### IX. Client-Side Behavior (TypeScript, Precompiled)
Component behaviors (e.g., sidebar toggle/collapse, dark/light theme toggle)
ARE allowed. All behavior code MUST be authored in TypeScript and compiled via
modern tooling (e.g., esbuild/tsc/rollup/swc). The package MUST ship fully
compiled JavaScript artifacts; end users MUST NOT be required to run a
bundler/transpiler to use the package.

Guidance:
- Optional integrators (e.g., django-vite) MAY be used internally, but the
	package MUST NOT depend on end-user build pipelines.
- Delivered bundles SHOULD be widely compatible (no runtime import maps/ESM
	assumptions unless a compatible fallback is also provided).
- Progressive enhancement: Core navigation and layout MUST remain usable without
	JavaScript; behaviors enhance when JS is available.

## Additional Constraints

- Layout Modes: The configuration MUST support three modes: navbar-only,
	sidebar-only, and sidebar+navbar. Mode selection MUST govern navigation
	rendering per Principle III.
- Menu System: Site navigation MUST be produced via django-flex-menus (or a
	compatible adapter), with a single authoritative menu tree. The renderer
	selects which mount point to display based on layout mode.
- Namespacing: Core layout CSS MUST be namespaced to avoid collisions with
	third-party frameworks. Layout MUST NOT rely on external utility classes to
	achieve structure.
- Template Overrides: Core templates are designed to be extended, not copied.
	End users SHOULD extend the standard layout templates rather than override
	internal structure.
- Component Libraries: A library MUST declare the subcomponents it implements
	and adhere to the component contract; breaking changes to that contract are
	MAJOR.
- Performance: Asset compilation SHOULD be incremental and cache-aware.
 - JavaScript Delivery: Compiled JS MUST be included under the package’s static
	 assets and load without requiring an external bundler at runtime. Source maps
	 MAY be shipped for debugging.

## Development Workflow

- Template-Only Inner Layout: Authors declare inner layout via component
	attributes in templates; there are no mixin or global controls for inner
	layout.
- Configuration Flow: Outer layout is configured centrally (settings-driven);
	inner layout is template-scoped. Do not conflate the two.
- Testing Gates (Constitution Check):
	- Gate A: No duplicate navigation across navbar/sidebar for selected mode.
	- Gate B: Layout renders without any CSS framework present.
	- Gate C: Inner layout regions reflect template attributes only; no alternate
		configuration path exists; no duplication or conflict is present.
	- Gate D: Basic accessibility landmarks and keyboard focus order present.
	- Gate E: Theming works via both Sass (build-time) and CSS variables
		(runtime) in sample pages.
	- Gate F: Compiled JS assets are present and functional without any external
		bundler; core layout remains usable with JS disabled.
- Release Versioning: Semantic Versioning applies to configuration structure and
	component library contracts:
	- MAJOR: Breaking changes to settings schema or component contracts.
	- MINOR: New non-breaking configuration options or components.
	- PATCH: Bug fixes, clarifications, or non-functional refinements.
 - Client-Side Build: TypeScript sources live with the component library; JS is
 	compiled during package build/release. Validate that compiled assets load via
 	Django staticfiles without any external bundler.

## Governance

- Supremacy: This constitution governs project structure, layout behavior,
	configuration, and release discipline. It supersedes ad-hoc practices.
- Amendments: Changes REQUIRE a brief design note describing the rationale,
	migration impact, and version bump. Document the amendment in the changelog.
- Review: PRs MUST include a "Constitution Check" outcome referencing the
	gates in Development Workflow. Reviewers MUST block if gates fail.
- Compliance: Quarterly review SHOULD validate that sample pages still satisfy
	accessibility, responsiveness, and navigation rules after dependency updates.

**Version**: 3.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-23
