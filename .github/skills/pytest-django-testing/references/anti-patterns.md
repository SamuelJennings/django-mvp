# Anti-Patterns

Common mistakes when writing FairDM tests, with corrections.

---

## ❌ Using unittest.TestCase

```python
# WRONG
import unittest

class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = ProjectFactory()

    def test_name(self):
        self.assertEqual(self.project.name, "Test")
```

```python
# CORRECT
import pytest
from fairdm.factories import ProjectFactory

@pytest.mark.django_db
class TestProject:
    def test_name(self):
        project = ProjectFactory()
        assert project.name  # use plain assert
```

---

## ❌ Layer Subdirectories

```
# WRONG
tests/unit/test_core/test_project/test_models.py
tests/integration/test_core/test_project/test_models.py
```

```
# CORRECT — flat mirror, no layer separation
tests/test_core/test_project/test_models.py
```

Unit and integration tests for a module live in the same file.

---

## ❌ Importing Factories from tests.factories

```python
# WRONG
from tests.factories import ProjectFactory
```

```python
# CORRECT
from fairdm.factories import ProjectFactory
```

---

## ❌ Wall-Clock Timing Assertions

```python
# WRONG
import time

def test_performance():
    start = time.time()
    do_thing()
    assert time.time() - start < 0.5  # flaky, machine-dependent
```

```python
# CORRECT — use query-count guards
def test_performance(django_assert_num_queries):
    with django_assert_num_queries(3):
        do_thing()
```

---

## ❌ Missing @pytest.mark.django_db

```python
# WRONG — will fail with "Database access not allowed"
class TestProject:
    def test_create(self):
        ProjectFactory()
```

```python
# CORRECT
@pytest.mark.django_db
class TestProject:
    def test_create(self):
        ProjectFactory()
```

---

## ❌ Manually Creating Related Objects When a Factory Exists

```python
# WRONG
from fairdm.contrib.contributors.models import Organization

def test_project():
    owner = Organization.objects.create(name="Org")
    project = Project.objects.create(name="P", owner=owner, ...)
```

```python
# CORRECT
from fairdm.factories import ProjectFactory

def test_project():
    project = ProjectFactory()  # factory handles owner via SubFactory
```

Only use `objects.create()` when you need to assert specific field values.

---

## ❌ Deep Fixture Chains

```python
# WRONG — hard to follow, implicit dependencies
@pytest.fixture
def org():
    return OrganizationFactory()

@pytest.fixture
def user(org):
    return UserFactory(organization=org)

@pytest.fixture
def project(user):
    return ProjectFactory(owner=user.organization)

@pytest.fixture
def dataset(project):
    return DatasetFactory(project=project)

def test_something(dataset):  # what does this give me?
    pass
```

```python
# CORRECT — explicit and readable
def test_something():
    project = ProjectFactory()
    dataset = DatasetFactory(project=project)
    # clear what's being set up
```

Use fixtures for expensive shared setup. Prefer inline factory calls for clarity.

---

## ❌ Hardcoded URLs

```python
# WRONG
response = client.get("/projects/1/")
```

```python
# CORRECT
from django.urls import reverse

response = client.get(reverse("project-detail", kwargs={"pk": project.pk}))
```

---

## ❌ Cross-Test State Leakage

```python
# WRONG — tests depend on execution order
_cache = {}

class TestCaching:
    def test_populate(self):
        _cache["key"] = "value"

    def test_read(self):
        assert _cache["key"] == "value"  # fails if run in isolation
```

Each test must be fully independent.

---

## ❌ Testing Django/Third-Party Internals

```python
# WRONG — testing Django's CharField, not your code
def test_charfield_max_length():
    field = Project._meta.get_field("name")
    assert field.max_length == 255
```

Test your business logic, constraints, and custom methods — not framework behaviour.
Exception: testing custom fields in `fairdm/db/` is appropriate.

---

## ❌ Commented-Out or Skipped Tests Without Reason

```python
# WRONG
# def test_something():
#     pass

@pytest.mark.skip  # no reason given
def test_other():
    pass
```

```python
# CORRECT — if skipping, explain why
@pytest.mark.skip(reason="Blocked by #123 — API not yet stable")
def test_other():
    pass
```

Delete dead tests. Don't comment them out.
