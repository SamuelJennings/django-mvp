<!--
Sync Impact Report
- Version change: 2.0.0 → 3.0.0
- Modified principles:
  - I. Design-First, Verify Implementation — expanded with story-level validation mandates
    (task grouping by user story, python manage.py check, pytest by story area)
  - IV. Compatibility & Config-Driven Design — expanded with cotton-only UI config mandate
  - VI. UI Verification (chrome-devtools-mcp) → VI. UI Verification (playwright-mcp)
    [BREAKING: agent tool requirement changed from chrome-devtools-mcp to playwright-mcp]
  - VIII. End-to-End Testing (playwright) — clarified distinction from Principle VI
- Added sections: none
- Removed sections: none
- Templates requiring updates:
  - ✅ .specify/templates/tasks-template.md (verification tasks updated to playwright-mcp;
    added python manage.py check + story-scoped pytest validation tasks per user story)
  - ✅ .specify/templates/plan-template.md (Constitution Check updated: playwright-mcp,
    cotton-only config, story validation)
  - ✅ .specify/templates/spec-template.md (no changes needed)
- Runtime guidance docs requiring updates:
  - ⚠ CONTRIBUTING.md (manual: update references from chrome-devtools-mcp to playwright-mcp)
- Follow-up TODOs: none
-->

# Django MVP Constitution

## Core Principles

### I. Design-First, Verify Implementation (NON-NEGOTIABLE)

All behavior changes MUST follow a design-verify-test workflow to ensure alignment between expectations and implementation.

**Rationale**: Front-end specifications are difficult to communicate precisely through written descriptions alone. Implementing design first allows for visual verification and user feedback before investing time in test design. This reduces wasted effort on tests for designs that don't match user expectations.

**Workflow**:

1. **Design Phase**: Create the design (mockups, wireframes, or initial implementation) based on specifications
2. **Verification Phase**: Verify the design meets expectations using visual inspection
   (Playwright MCP server for UI), user feedback, and manual testing
3. **Implementation Phase**: Refine implementation based on verification feedback
4. **Testing Phase**: Write comprehensive tests for the verified, approved implementation

**Testing Requirements** (after design verification):

- All new or changed Python behavior MUST have pytest coverage
- Django integration behavior MUST have pytest-django coverage
- Cotton component tests MUST use `django_cotton.cotton_render()` with pytest-django's `rf` fixture (NOT Template() or render_to_string)
- User-visible/UI behavior MUST have pytest-playwright coverage when the change affects rendered output, interactions, or accessibility
- Pull requests MUST NOT be merged with failing tests, or without new/updated tests for behavior changes
- The only acceptable exception is a docs-only change (no runtime behavior impact)

**Story-Level Validation (NON-NEGOTIABLE)**:

- **Task Breakdown**: Tasks (`tasks.md`) MUST be grouped by user story so that each story
  can be implemented and tested independently where feasible. Shared foundational work
  MUST be captured as explicit blocking tasks. Every phase in `tasks.md` that modifies
  any Django code (models, views, forms, URLs, settings, migrations, templates) MUST
  include an explicit validation task running `python manage.py check` AND the pytest
  suite for the touched area (e.g., `pytest tests/test_views/` after a view phase).
  These validation tasks are REQUIRED regardless of which tool or agent generates
  `tasks.md`; they MUST NOT be omitted when regenerating, updating, or re-ordering
  task files. The hardcoded equivalent in any CLI tooling is a convenience, not a
  substitute for this constitutional mandate.
- **Test-First Discipline**: Tests MUST be written and observed failing before
  implementation begins. No change MAY be merged that causes the agreed test suite
  for the touched area to fail.
- **System Checks**: `python manage.py check` MUST pass after completing each user story
  or major phase; model errors, admin field references, and misconfiguration MUST be
  caught before they reach staging.
- **Validation Frequency**: For multi-phase implementations, run system checks after each
  phase and update documentation incrementally.

### II. Documentation-First

Documentation is part of the product surface area.

- Every public setting, template block, and component MUST be documented with at least one minimal usage example.
- Any change to public behavior MUST include a docs update in the same pull request.
- Examples MUST be kept working and reflect the current recommended usage.
- Docs MUST describe expected behavior in testable terms (inputs, outputs, and constraints).

### III. Component Quality & Accessibility

Components MUST be usable, accessible, and predictable.

- Components MUST render valid, semantic HTML.
- Components MUST be accessible by default (keyboard navigable where relevant, with appropriate ARIA when necessary).
- If a change affects markup structure, add/update tests that assert the rendered HTML contract.
- UI behavior changes SHOULD be covered by browser tests when feasible.

### IV. Compatibility & Config-Driven Design

This is a reusable Django app; upgrades and consumers matter.

- Prefer configuration and extension points over invasive template overrides.
- Breaking changes MUST be avoided; if unavoidable, they MUST be explicit, documented, and versioned.
- Default behavior MUST remain stable across minor releases.
- **Cotton-Only UI Configuration**: UI configuration and customization MUST be achieved
  exclusively through Django Cotton components and template-level overrides. Python-level
  configuration is reserved for structural settings (e.g., installed apps, database,
  middleware). No CSS/JS wiring, layout selection, or component behavior MAY be
  configured through Python code when a Cotton component attribute or slot override is
  sufficient.

### V. Tooling & Consistency

The project uses consistent tooling to keep quality high and contributions smooth.

- Project commands MUST run through Poetry (e.g., `poetry run pytest`).
- Code MUST satisfy linting/formatting and any configured static checks before merge.
- Keep changes minimal and focused; avoid incidental refactors.

### VI. UI Verification (playwright-mcp)

Agents MUST verify UI changes using the Playwright MCP server during implementation.

- When building or modifying UI elements, agents MUST use the Playwright MCP server to
  open a real browser, interact with the rendered output, and confirm that implementation
  changes are visually and interactively represented as expected.
- Any phase in `tasks.md` that modifies the user experience — including HTML templates,
  Cotton components, form rendering, CSS, HTMX interactions, or any visible UI element —
  MUST include at least one Playwright verification task that uses the Playwright MCP
  server to confirm the expected interactive or visual outcome in a real browser.
- Playwright tasks MUST assert the specific UX behaviour described in the corresponding
  user story acceptance criteria (e.g., "the form displays an inline validation error
  adjacent to the field", "the delete confirmation modal appears") and MUST NOT merely
  assert that the page loads without error.
- Visual verification MUST occur after each significant UI modification to catch
  rendering issues before they are committed.
- This requirement applies to all `tasks.md` files regardless of which agent or tool
  generates them.

### VII. Documentation Retrieval (context7)

Agents MUST use current documentation when working with dependencies.

- Agents MUST use context7 to retrieve up-to-date documentation for all packages and libraries they are working with.
- This ensures that code follows current API patterns and best practices rather than outdated examples.
- Context7 MUST be consulted before implementing features that rely on external libraries (Django, Cotton, Bootstrap, etc.).

### VIII. End-to-End Testing (pytest-playwright)

Features MUST include comprehensive end-to-end test coverage using pytest-playwright.

- All new features MUST include end-to-end tests using pytest-playwright to verify
  complete user workflows.
- E2E tests MUST cover the entire user journey from initial page load through final
  action completion.
- UI interactions, form submissions, navigation flows, and visual elements MUST be
  tested at the browser level.
- E2E tests serve as acceptance tests that validate feature requirements are fully met.
- **Distinction from Principle VI**: Playwright MCP server tasks (Principle VI) are the
  inline interactive verification step performed by agents during implementation;
  pytest-playwright tests (this principle) are the formal regression suite that persists
  in the repository and runs in CI.

## Quality Gates

The following gates MUST pass for every pull request that changes runtime behavior:

- Unit/integration tests pass (`pytest` via Poetry).
- Linting passes (Ruff).
- Formatting is applied (Ruff formatter).
- Documentation is updated when public behavior changes.
- `python manage.py check` passes with no errors.

If a change affects UI output or interaction, add or update pytest-playwright coverage.

## Development Workflow

- Start with the design that expresses the desired behavior and visual appearance
- Verify the design meets expectations through visual inspection and user feedback (use
  Playwright MCP server for UI verification)
- Refine the implementation based on verification feedback
- Write comprehensive tests for the verified implementation (unit, integration, and end-to-end)
- After each user story phase, run `python manage.py check` and the relevant pytest suite
- Update documentation alongside the change, not after
- Keep PRs small and reviewable; split unrelated changes

## Governance

This constitution defines non-negotiable project rules and supersedes local conventions.

- Amendments MUST be proposed via pull request and include a brief rationale.
- Amendments MUST state whether they are MAJOR/MINOR/PATCH changes to this constitution.
- Any PR that materially changes development norms MUST update this constitution and any dependent templates.
- Reviews MUST explicitly check compliance with the Core Principles.

### Versioning Policy (Constitution)

- MAJOR: Removes or redefines a principle in a backward-incompatible way.
- MINOR: Adds a principle/section or materially expands guidance.
- PATCH: Clarifies wording or fixes typos without changing intent.

**Version**: 3.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-04-14
