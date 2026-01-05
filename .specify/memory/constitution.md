<!--
Sync Impact Report
- Version change: unversioned template → 1.0.0
- Modified principles:
	- Principle 1 placeholder → I. Test-First (NON-NEGOTIABLE)
	- Principle 2 placeholder → II. Documentation-First
	- Principle 3 placeholder → III. Component Quality & Accessibility
	- Principle 4 placeholder → IV. Compatibility & Config-Driven Design
	- Principle 5 placeholder → V. Tooling & Consistency
- Added sections: none (filled existing template)
- Removed sections: none
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (✅ updated)
	- ✅ .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: none
-->

# Django MVP Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)

All behavior changes MUST be driven by tests written first.

- Tests MUST be written and observed failing before implementation work begins (Red → Green → Refactor).
- All new or changed Python behavior MUST have pytest coverage.
- Django integration behavior MUST have pytest-django coverage.
- User-visible/UI behavior MUST have pytest-playwright coverage when the change affects rendered output, interactions, or accessibility.
- Pull requests MUST NOT be merged with failing tests, or without new/updated tests for behavior changes.
- The only acceptable exception is a docs-only change (no runtime behavior impact).

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

## Quality Gates

The following gates MUST pass for every pull request that changes runtime behavior:

- Unit/integration tests pass (`pytest` via Poetry).
- Linting passes (Ruff).
- Formatting is applied (Ruff formatter).
- Documentation is updated when public behavior changes.

If a change affects UI output or interaction, add or update pytest-playwright coverage.

## Development Workflow

- Start with the smallest failing test that expresses the desired behavior.
- Implement the minimal code to make the test pass.
- Refactor only after the tests are green.
- Update documentation alongside the change, not after.
- Keep PRs small and reviewable; split unrelated changes.

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

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
