<!--
Sync Impact Report
- Version change: 1.1.0 → 2.0.0
- Modified principles:
	- I. Test-First → I. Design-First, Verify Implementation (BREAKING CHANGE)
- Added sections: none
- Removed sections: none
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (updated constitution check to reflect design-first workflow)
	- ✅ .specify/templates/tasks-template.md (updated task ordering: design → implement → verify → test)
	- ✅ .specify/templates/spec-template.md (no changes needed - already emphasizes design)
- Runtime guidance docs requiring updates:
	- ✅ CONTRIBUTING.md (updated core principles and PR process to reflect design-first approach)
- Follow-up TODOs: none
-->

# Django MVP Constitution

## Core Principles

### I. Design-First, Verify Implementation (NON-NEGOTIABLE)

All behavior changes MUST follow a design-verify-test workflow to ensure alignment between expectations and implementation.

**Rationale**: Front-end specifications are difficult to communicate precisely through written descriptions alone. Implementing design first allows for visual verification and user feedback before investing time in test design. This reduces wasted effort on tests for designs that don't match user expectations.

**Workflow**:

1. **Design Phase**: Create the design (mockups, wireframes, or initial implementation) based on specifications
2. **Verification Phase**: Verify the design meets expectations using visual inspection (chrome-devtools-mcp for UI), user feedback, and manual testing
3. **Implementation Phase**: Refine implementation based on verification feedback
4. **Testing Phase**: Write comprehensive tests for the verified, approved implementation

**Testing Requirements** (after design verification):

- All new or changed Python behavior MUST have pytest coverage
- Django integration behavior MUST have pytest-django coverage
- Cotton component tests MUST use `django_cotton.cotton_render()` with pytest-django's `rf` fixture (NOT Template() or render_to_string)
- User-visible/UI behavior MUST have pytest-playwright coverage when the change affects rendered output, interactions, or accessibility
- Pull requests MUST NOT be merged with failing tests, or without new/updated tests for behavior changes
- The only acceptable exception is a docs-only change (no runtime behavior impact)

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

### V. Tooling & Consistency

The project uses consistent tooling to keep quality high and contributions smooth.

- Project commands MUST run through Poetry (e.g., `poetry run pytest`).
- Code MUST satisfy linting/formatting and any configured static checks before merge.
- Keep changes minimal and focused; avoid incidental refactors.

### VI. UI Verification (chrome-devtools-mcp)

Agents MUST verify UI changes are properly reflected during implementation.

- When building or modifying UI elements, agents MUST use chrome-devtools-mcp to inspect the rendered output and confirm that implementation changes are visually represented in the browser.
- Visual verification MUST occur after each significant UI modification to catch rendering issues early.
- This ensures that template changes, CSS updates, and component modifications produce the expected visual results.

### VII. Documentation Retrieval (context7)

Agents MUST use current documentation when working with dependencies.

- Agents MUST use context7 to retrieve up-to-date documentation for all packages and libraries they are working with.
- This ensures that code follows current API patterns and best practices rather than outdated examples.
- Context7 MUST be consulted before implementing features that rely on external libraries (Django, Cotton, Bootstrap, etc.).

### VIII. End-to-End Testing (playwright)

Features MUST include comprehensive end-to-end testing.

- All new features MUST include end-to-end tests using playwright to verify complete user workflows.
- E2E tests MUST cover the entire user journey from initial page load through final action completion.
- UI interactions, form submissions, navigation flows, and visual elements MUST be tested at the browser level.
- E2E tests serve as acceptance tests that validate feature requirements are fully met.

## Quality Gates

The following gates MUST pass for every pull request that changes runtime behavior:

- Unit/integration tests pass (`pytest` via Poetry).
- Linting passes (Ruff).
- Formatting is applied (Ruff formatter).
- Documentation is updated when public behavior changes.

If a change affects UI output or interaction, add or update pytest-playwright coverage.

## Development Workflow

- Start with the design that expresses the desired behavior and visual appearance
- Verify the design meets expectations through visual inspection and user feedback (use chrome-devtools-mcp for UI verification)
- Refine the implementation based on verification feedback
- Write comprehensive tests for the verified implementation (unit, integration, and end-to-end)
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

**Version**: 2.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-19
