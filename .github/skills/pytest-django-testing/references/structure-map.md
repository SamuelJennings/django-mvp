# Structure Map

Complete mapping from `fairdm/` source modules to their `tests/` counterparts.

## Rule

Every `fairdm/<path>/<module>.py` maps to `tests/test_<path>/test_<module>.py`.
Directory names get `test_` prefixes. Files get `test_` prefixes.

## Current Mapping

```text
SOURCE                                    TEST
─────────────────────────────────────     ─────────────────────────────────────────────
fairdm/plugins.py                      →  tests/test_plugins.py
fairdm/config.py                       →  tests/test_config.py
fairdm/views.py                        →  tests/test_views.py

fairdm/conf/                           →  tests/test_conf/
fairdm/conf/settings/                  →  tests/test_conf/ (flat — settings tests here)

fairdm/core/project/models.py          →  tests/test_core/test_project/test_models.py
fairdm/core/project/forms.py           →  tests/test_core/test_project/test_forms.py
fairdm/core/project/admin.py           →  tests/test_core/test_project/test_admin.py
fairdm/core/project/views.py           →  tests/test_core/test_project/test_views.py

fairdm/core/dataset/models.py          →  tests/test_core/test_dataset/test_models.py
fairdm/core/dataset/forms.py           →  tests/test_core/test_dataset/test_forms.py
fairdm/core/dataset/admin.py           →  tests/test_core/test_dataset/test_admin.py
fairdm/core/dataset/filters.py         →  tests/test_core/test_dataset/test_filters.py

fairdm/core/sample/models.py           →  tests/test_core/test_sample/test_models.py
fairdm/core/sample/admin.py            →  tests/test_core/test_sample/test_admin.py

fairdm/core/measurement/models.py      →  tests/test_core/test_measurement/test_models.py
fairdm/core/measurement/admin.py       →  tests/test_core/test_measurement/test_admin.py

fairdm/contrib/contributors/models.py  →  tests/test_contrib/test_contributors/test_models.py
fairdm/contrib/contributors/utils/     →  tests/test_contrib/test_contributors/test_utils.py
fairdm/contrib/contributors/views/     →  tests/test_contrib/test_contributors/test_views.py

fairdm/contrib/plugins/                →  tests/test_contrib/test_plugins/

fairdm/db/fields.py                    →  tests/test_db/test_fields.py
fairdm/db/partial_date_field.py        →  tests/test_db/test_partial_date_field.py

fairdm/registry/config.py              →  tests/test_registry/test_config.py
fairdm/registry/admin.py               →  tests/test_registry/test_admin.py
fairdm/registry/validation.py          →  tests/test_registry/test_validation.py

fairdm/factories/                      →  tests/test_factories/
```

## Directories That Do NOT Get Tests

These contain no testable Python logic:

- `fairdm/static/` — CSS, JS, images
- `fairdm/templates/` — HTML templates (tested via view tests)
- `fairdm/fixtures/` — JSON/YAML data fixtures
- `fairdm/management/` — management commands (tested in test_management/)
- `*/migrations/` — auto-generated, never tested directly

## Shared Test Infrastructure

```text
tests/
├── __init__.py
├── conftest.py              — session-level DB setup
├── settings.py              — test-specific Django settings
└── fixtures/
    └── pytest_fixtures.py   — reusable composed fixtures (user, project, etc.)
```

Subdirectory-specific fixtures go in `tests/test_<dir>/conftest.py`.

## Adding a New Module

1. Identify the source path: `fairdm/<app>/<module>.py`
2. Create test path: `tests/test_<app>/test_<module>.py`
3. Add `__init__.py` in any new directories
4. Follow the exemplar patterns in [exemplar-patterns.md](exemplar-patterns.md)
