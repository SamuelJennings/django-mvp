---
name: pytest-django-testing
description: >-
  Write, review, and maintain tests for Django projects using pytest. Use when asked to create
  new tests, add test coverage for a module, review existing tests, fix failing tests, or
  refactor test code. Covers pytest conventions, factory-boy usage, fixture design, test
  structure (flat mirror of source tree), Django model/form/view/admin testing patterns,
  and performance guard patterns using query-count assertions. Also use when discussing
  testing strategy, test organization, or when creating new modules that need accompanying tests.
---

# Pytest Django Testing

## Stack

- **pytest** + **pytest-django** — test runner and Django integration
- **factory-boy** — model instance generation (recommended)
- **Coverage.py** — coverage reporting (configured in pyproject.toml)

Never use `unittest`, `TestCase`, or `setUp/tearDown` patterns. Use pytest exclusively.

## Directory Structure

Tests mirror the source tree with `test_` prefixes:

```
myapp/core/models.py          → tests/test_core/test_models.py
myapp/contrib/module/         → tests/test_contrib/test_module/
myapp/utils/helpers.py        → tests/test_utils/test_helpers.py
myapp/plugins.py              → tests/test_plugins.py
myapp/db/fields.py            → tests/test_db/test_fields.py
```

**Rules:**

- Test directories: `test_<dirname>/`
- Test files: `test_<module>.py`
- Every directory needs an `__init__.py`
- No layer separation (no `unit/`, `integration/`, `contract/` subdirectories)
- Unit and integration tests for a module live together in the same file
- Mirror the source structure exactly to make tests easy to locate

**Benefits:**

- Predictable test location: if you know where the source is, you know where the test is
- Clear ownership: each module has exactly one corresponding test file
- No confusion about where to add new tests
- Easy navigation between source and tests

## Running Tests

```bash
poetry run pytest                          # all tests
poetry run pytest tests/test_core/         # one subtree
poetry run pytest -k "test_project"        # by name
poetry run pytest -m slow                  # only slow-marked tests
poetry run pytest --no-header -q           # quiet output
poetry run pytest --cov=myapp --cov-report=html  # with coverage
```

## Factories (factory-boy)

If using factory-boy for model instance generation:

```python
from myapp.factories import (
    UserFactory, ProjectFactory, DocumentFactory
)

# Basic usage
user = UserFactory()
project = ProjectFactory(owner=user)

# With relationships
project = ProjectFactory(documents=3)  # Creates 3 related documents

# Batch creation
projects = ProjectFactory.create_batch(5)

# Custom attributes
user = UserFactory(email="custom@example.com")
```

### Factory Best Practices

- **SubFactory** for FK relations — never manually create parent objects when a factory exists
- **Sequence** for unique fields: `factory.Sequence(lambda n: f"value{n}")`
- **create_batch(n)** for bulk creation
- **Traits** for alternate configurations
- **Opt-in pattern** for related objects — by default, create minimal required data only

### Factory Opt-In Pattern

Best practice: factories should create only required fields by default. Related objects should be opt-in:

```python
# Minimal (no related objects) - DEFAULT behavior
project = ProjectFactory()
assert project.documents.count() == 0

# With related objects (opt-in via kwargs)
project = ProjectFactory(documents=2)
assert project.documents.count() == 2

# Custom attributes for related objects
project = ProjectFactory(
    documents=3,
    documents__status="published"
)
```

**Why Opt-In?**

1. **Prevents constraint violations** — Auto-creating related objects can cause unique constraint violations
2. **Minimizes test data** — Most tests don't need full object graphs
3. **Explicit control** — When you need related objects, you explicitly control count and attributes
4. **Faster tests** — Fewer DB inserts means faster test execution

## Fixtures

### Built-in pytest-django fixtures

Use directly — no need to redeclare:

- `db` — marks test as needing database access
- `transactional_db` — provides transactional database access
- `client` — Django test client
- `rf` — RequestFactory
- `admin_user` — superuser instance
- `django_user_model` — User model class
- `django_assert_num_queries` — query count assertion context manager
- `settings` — modify Django settings for a test

### Custom Project Fixtures

Define reusable fixtures in `conftest.py` files:

```python
# tests/conftest.py
import pytest
from myapp.factories import UserFactory, ProjectFactory

@pytest.fixture
def user(db):
    """Standard user instance."""
    return UserFactory()

@pytest.fixture
def project(user):
    """Project with owner."""
    return ProjectFactory(owner=user)

@pytest.fixture
def project_with_documents(project):
    """Project with 3 documents."""
    return project, ProjectFactory.create_batch(3, project=project)
```

**Fixture Guidelines:**

- Keep fixtures focused and single-purpose
- Prefer factory calls over complex fixture setup
- Use `conftest.py` for fixtures shared across multiple test files
- Use fixture scope (`function`, `class`, `module`, `session`) appropriately
- Document fixture behavior in docstrings

## Test Organization

Group tests into classes by subject. One class per logical unit under test:

```python
@pytest.mark.django_db
class TestProjectModel:
    """Tests for Project model behavior."""

    def test_creation_with_required_fields(self):
        """Project can be created with only required fields."""
        ...

    def test_uuid_is_unique(self):
        """Each project gets a unique UUID."""
        ...

    def test_status_choices(self):
        """Status field accepts only valid choices."""
        ...

@pytest.mark.django_db
class TestProjectCreateForm:
    """Tests for ProjectCreateForm validation and behavior."""

    def test_valid_with_required_fields(self):
        """Form is valid with all required fields."""
        ...

    def test_invalid_without_name(self):
        """Form is invalid without project name."""
        ...
```

**Class Naming:** `Test<SubjectName>`
**Method Naming:** `test_<what_is_being_tested>` — descriptive, no abbreviations

- `@pytest.mark.django_db` on every class or function that touches the database
- **Arrange–Act–Assert** pattern, separated by blank lines
- One logical assertion per test (unless tightly coupled)
- Deterministic and isolated — no cross-test state, no time-dependent logic
- `@pytest.mark.parametrize` for repeated logic with different inputs
- `@pytest.mark.slow` for tests that take >1 second

### Example Test Structure

```python
@pytest.mark.django_db
class TestProjectModel:
    def test_project_creation(self):
        """Projects can be created with valid data."""
        # Arrange
        user = UserFactory()

        # Act
        project = ProjectFactory(owner=user, name="Test Project")

        # Assert
        assert project.name == "Test Project"
        assert project.owner == user
        assert project.pk is not None
```

## Performance Tests

**Never** use wall-clock timing assertions (`assert elapsed < 0.1`). They are flaky and environment-dependent.

Use query-count guards instead:

```python
def test_list_view_query_count(client, django_assert_num_queries):
    """List view should use constant queries regardless of item count."""
    ProjectFactory.create_batch(10)

    with django_assert_num_queries(3):
        response = client.get("/projects/")

    assert response.status_code == 200
```

Or algorithmic complexity guards (assert O(n) not O(n²)):

```python
def test_bulk_operation_scales_linearly():
    """Bulk operation should scale linearly with input size."""
    # Test with n=10
    start = time.time()
    process_batch(10)
    time_10 = time.time() - start

    # Test with n=20 (should be ~2x, not 4x)
    start = time.time()
    process_batch(20)
    time_20 = time.time() - start

    assert time_20 / time_10 < 2.5  # Allow some overhead
```

## Common Testing Patterns

### Model Tests

```python
@pytest.mark.django_db
class TestProjectModel:
    def test_required_fields(self):
        """Model requires name field."""
        with pytest.raises(ValidationError):
            Project.objects.create(name=None)

    def test_unique_constraint(self):
        """Project names must be unique per owner."""
        user = UserFactory()
        ProjectFactory(owner=user, name="Test")

        with pytest.raises(IntegrityError):
            ProjectFactory(owner=user, name="Test")

    def test_str_representation(self):
        """Model __str__ returns expected format."""
        project = ProjectFactory(name="Test Project")
        assert str(project) == "Test Project"
```

### Form Tests

```python
@pytest.mark.django_db
class TestProjectForm:
    def test_valid_data(self):
        """Form is valid with complete data."""
        form = ProjectForm(data={
            'name': 'Test Project',
            'description': 'Test description'
        })
        assert form.is_valid()

    def test_missing_required_field(self):
        """Form is invalid without required name field."""
        form = ProjectForm(data={'description': 'Test'})
        assert not form.is_valid()
        assert 'name' in form.errors
```

### View Tests

```python
@pytest.mark.django_db
class TestProjectListView:
    def test_get_returns_200(self, client):
        """List view returns 200 OK."""
        response = client.get("/projects/")
        assert response.status_code == 200

    def test_displays_projects(self, client):
        """List view displays all projects."""
        projects = ProjectFactory.create_batch(3)

        response = client.get("/projects/")

        for project in projects:
            assert project.name in response.content.decode()

    def test_requires_authentication(self, client):
        """List view redirects unauthenticated users."""
        response = client.get("/projects/")
        assert response.status_code == 302
```

### Admin Tests

```python
@pytest.mark.django_db
class TestProjectAdmin:
    def test_model_registered(self):
        """Project is registered in admin."""
        from django.contrib import admin
        assert Project in admin.site._registry

    def test_list_display(self, admin_client):
        """Admin list page displays expected columns."""
        ProjectFactory.create_batch(2)

        response = admin_client.get("/admin/myapp/project/")

        assert response.status_code == 200
        assert b'name' in response.content
        assert b'created_at' in response.content
```

## Parametrized Tests

Use `@pytest.mark.parametrize` to test multiple inputs:

```python
@pytest.mark.parametrize("status,expected_queryset_count", [
    ("draft", 2),
    ("published", 3),
    ("archived", 1),
])
@pytest.mark.django_db
def test_filter_by_status(status, expected_queryset_count):
    """Filtering by status returns correct count."""
    ProjectFactory.create_batch(2, status="draft")
    ProjectFactory.create_batch(3, status="published")
    ProjectFactory.create_batch(1, status="archived")

    result = Project.objects.filter(status=status)
    assert result.count() == expected_queryset_count
```

## What NOT to Do

**❌ Don't use unittest patterns:**

```python
# BAD
class TestProject(unittest.TestCase):
    def setUp(self): ...
    def tearDown(self): ...
```

**❌ Don't manually create objects when factories exist:**

```python
# BAD
user = User.objects.create(username="test", email="test@example.com")

# GOOD
user = UserFactory()
```

**❌ Don't share state between tests:**

```python
# BAD - module-level shared state
PROJECT = None

def test_create_project():
    global PROJECT
    PROJECT = ProjectFactory()

def test_update_project():
    global PROJECT  # Depends on previous test!
    PROJECT.name = "Updated"
```

**❌ Don't use time-based assertions:**

```python
# BAD - flaky, environment-dependent
start = time.time()
expensive_operation()
assert time.time() - start < 1.0

# GOOD - count queries instead
with django_assert_num_queries(5):
    expensive_operation()
```

**❌ Don't test Django's functionality:**

```python
# BAD - testing Django, not your code
def test_foreign_key_works():
    user = UserFactory()
    project = ProjectFactory(owner=user)
    assert project.owner.pk == user.pk
```

## Test Settings Configuration

Key configuration for `tests/settings.py` (or similar):

```python
# Use in-memory SQLite for speed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster test setup
class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Fast password hashing (insecure, but fast for tests)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
```

## Checklist for New Tests

1. ✅ Identify the source module → derive test file path from mirror structure
2. ✅ Create test file with `__init__.py` in any new directories
3. ✅ Import factories for model instances (or create if none exist)
4. ✅ Group tests in classes by subject (`TestXxxModel`, `TestXxxForm`, etc.)
5. ✅ Mark DB-accessing tests with `@pytest.mark.django_db`
6. ✅ Use Arrange-Act-Assert structure with blank line separation
7. ✅ Write descriptive test names explaining what is tested
8. ✅ Run `poetry run pytest <test_file>` to verify
9. ✅ Check coverage: `poetry run pytest --cov=myapp --cov-report=html`
10. ✅ Ensure coverage does not decrease

## Continuous Improvement

- **Refactor tests** as you refactor code — tests are code too
- **Delete obsolete tests** when removing features
- **Update tests first** when fixing bugs (TDD approach)
- **Keep tests fast** — slow tests don't get run
- **Review test quality** in code reviews, not just production code

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)
- [factory-boy documentation](https://factoryboy.readthedocs.io/)
- [Django testing documentation](https://docs.djangoproject.com/en/stable/topics/testing/)

---

**Remember:** Good tests are:

- **Fast** — run in milliseconds
- **Independent** — no shared state
- **Repeatable** — same result every time
- **Self-validating** — pass or fail clearly
- **Timely** — written with or before code
