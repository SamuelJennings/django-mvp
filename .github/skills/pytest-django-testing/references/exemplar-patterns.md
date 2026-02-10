# Exemplar Test Patterns

Concrete, copy-paste-ready patterns for each test category.

## Table of Contents

- [Model Tests](#model-tests)
- [Form Tests](#form-tests)
- [View Tests](#view-tests)
- [Admin Tests](#admin-tests)
- [Filter Tests](#filter-tests)
- [Registry Tests](#registry-tests)
- [Management Command Tests](#management-command-tests)

---

## Model Tests

Test creation, field validation, constraints, relationships, and custom methods.

```python
"""Tests for fairdm.core.project.models."""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from fairdm.core.project.models import Project, ProjectDate
from fairdm.core.choices import ProjectStatus
from fairdm.factories import OrganizationFactory, ProjectFactory
from fairdm.utils.choices import Visibility


@pytest.mark.django_db
class TestProjectModel:
    """Tests for Project model."""

    def test_creation_with_required_fields(self):
        owner = OrganizationFactory()
        project = Project.objects.create(
            name="Test Project",
            status=ProjectStatus.CONCEPT,
            visibility=Visibility.PRIVATE,
            owner=owner,
        )

        assert project.pk is not None
        assert project.name == "Test Project"
        assert project.uuid is not None

    def test_uuid_is_unique(self):
        p1 = ProjectFactory()
        p2 = ProjectFactory()

        assert p1.uuid != p2.uuid

    def test_uuid_prefix(self):
        project = ProjectFactory()

        assert project.uuid.startswith("p")

    def test_status_choices(self):
        """Parametrize when many values need the same assertion."""
        owner = OrganizationFactory()
        for status in [ProjectStatus.CONCEPT, ProjectStatus.PLANNING,
                       ProjectStatus.IN_PROGRESS, ProjectStatus.COMPLETE]:
            project = Project.objects.create(
                name=f"Project {status}",
                status=status,
                visibility=Visibility.PRIVATE,
                owner=owner,
            )
            assert project.status == status

    def test_str_returns_name(self):
        project = ProjectFactory(name="My Project")

        assert str(project) == "My Project"

    def test_unique_constraint_violation(self):
        """Test database-level constraints raise IntegrityError."""
        # Example: if a unique_together exists
        with pytest.raises(IntegrityError):
            # create duplicate...
            pass


@pytest.mark.django_db
class TestProjectDateModel:
    """Tests for ProjectDate related model."""

    def test_date_linked_to_project(self):
        project = ProjectFactory()
        date = ProjectDate.objects.create(project=project, type="created")

        assert date.project == project

    def test_cascade_delete(self):
        project = ProjectFactory()
        ProjectDate.objects.create(project=project, type="created")
        project.delete()

        assert ProjectDate.objects.count() == 0
```

### Key principles

- Use factories (`ProjectFactory()`) over manual `objects.create()` when the test
  doesn't care about specific field values.
- Use `objects.create()` when the test asserts specific field values.
- Test constraints with `pytest.raises(IntegrityError)` or `pytest.raises(ValidationError)`.
- Test cascade/set_null behaviour on FK deletion.

---

## Form Tests

Test valid/invalid submissions, field requirements, and business rule validation.

```python
"""Tests for fairdm.core.project.forms."""

import pytest

from fairdm.core.choices import ProjectStatus
from fairdm.core.project.forms import ProjectCreateForm
from fairdm.factories import OrganizationFactory
from fairdm.utils.choices import Visibility


@pytest.mark.django_db
class TestProjectCreateForm:

    def test_valid_with_required_fields(self):
        owner = OrganizationFactory()
        form = ProjectCreateForm(data={
            "name": "Test",
            "status": ProjectStatus.CONCEPT,
            "visibility": Visibility.PRIVATE,
            "owner": owner.pk,
        })

        assert form.is_valid(), f"Errors: {form.errors}"
        project = form.save()
        assert project.pk is not None

    def test_invalid_without_name(self):
        owner = OrganizationFactory()
        form = ProjectCreateForm(data={
            "status": ProjectStatus.CONCEPT,
            "visibility": Visibility.PRIVATE,
            "owner": owner.pk,
        })

        assert not form.is_valid()
        assert "name" in form.errors

    def test_blank_optional_field_is_accepted(self):
        owner = OrganizationFactory()
        form = ProjectCreateForm(data={
            "name": "Test",
            "status": ProjectStatus.CONCEPT,
            "visibility": Visibility.PRIVATE,
            "owner": owner.pk,
            "description": "",  # optional
        })

        assert form.is_valid()

    @pytest.mark.parametrize("name", ["", None])
    def test_name_cannot_be_blank_or_none(self, name):
        owner = OrganizationFactory()
        form = ProjectCreateForm(data={
            "name": name,
            "status": ProjectStatus.CONCEPT,
            "visibility": Visibility.PRIVATE,
            "owner": owner.pk,
        })

        assert not form.is_valid()
        assert "name" in form.errors
```

### Key principles

- Always pass `data=` explicitly.
- `form.is_valid()` → `form.errors` for debugging.
- Test both happy and sad paths.
- Use `@pytest.mark.parametrize` for repeated validation checks.

---

## View Tests

Test HTTP responses, permissions, redirects, and context data.

```python
"""Tests for project views."""

import pytest
from django.urls import reverse

from fairdm.factories import ProjectFactory, UserFactory


@pytest.mark.django_db
class TestProjectListView:

    def test_returns_200(self, client):
        response = client.get(reverse("project-list"))

        assert response.status_code == 200

    def test_context_contains_projects(self, client):
        ProjectFactory.create_batch(3)

        response = client.get(reverse("project-list"))

        assert len(response.context["object_list"]) == 3

    def test_unauthenticated_redirect(self, client):
        response = client.get(reverse("project-create"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestProjectDetailView:

    def test_returns_200_for_existing_project(self, client):
        project = ProjectFactory()

        response = client.get(
            reverse("project-detail", kwargs={"pk": project.pk})
        )

        assert response.status_code == 200

    def test_returns_404_for_nonexistent(self, client):
        response = client.get(
            reverse("project-detail", kwargs={"pk": 99999})
        )

        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectCreateView:

    def test_authenticated_user_can_create(self, client):
        user = UserFactory()
        client.force_login(user)

        response = client.get(reverse("project-create"))

        assert response.status_code == 200

    def test_post_creates_project(self, client):
        user = UserFactory()
        client.force_login(user)

        response = client.post(reverse("project-create"), data={
            "name": "New Project",
            # ... other required fields
        })

        assert response.status_code in (200, 302)
```

### Key principles

- Use `client` fixture from pytest-django (not `self.client`).
- Use `reverse()` for URL resolution — never hardcode paths.
- `client.force_login(user)` for authenticated tests.
- Check `response.status_code`, `response.context`, `response.url`.

---

## Admin Tests

Test admin registration, list display, and custom actions.

```python
"""Tests for project admin configuration."""

import pytest
from django.contrib.admin.sites import AdminSite

from fairdm.core.project.models import Project


@pytest.mark.django_db
class TestProjectAdmin:

    def test_model_is_registered(self):
        from django.contrib import admin

        assert Project in admin.site._registry

    def test_admin_list_page_loads(self, admin_client):
        response = admin_client.get("/admin/project/project/")

        assert response.status_code == 200

    def test_admin_add_page_loads(self, admin_client):
        response = admin_client.get("/admin/project/project/add/")

        assert response.status_code == 200
```

### Key principles

- Use `admin_client` fixture (pre-authenticated superuser).
- Test that pages load (200) — don't over-test admin internals.

---

## Filter Tests

Test django-filter filtersets and queryset filtering.

```python
"""Tests for project filters."""

import pytest

from fairdm.core.choices import ProjectStatus
from fairdm.factories import ProjectFactory


@pytest.mark.django_db
class TestProjectFilter:

    def test_filter_by_status(self):
        from fairdm.core.project.filters import ProjectFilter
        from fairdm.core.project.models import Project

        ProjectFactory(status=ProjectStatus.CONCEPT)
        ProjectFactory(status=ProjectStatus.COMPLETE)

        qs = Project.objects.all()
        f = ProjectFilter(data={"status": ProjectStatus.CONCEPT}, queryset=qs)

        assert f.qs.count() == 1
        assert f.qs.first().status == ProjectStatus.CONCEPT

    def test_empty_filter_returns_all(self):
        from fairdm.core.project.filters import ProjectFilter
        from fairdm.core.project.models import Project

        ProjectFactory.create_batch(5)

        f = ProjectFilter(data={}, queryset=Project.objects.all())

        assert f.qs.count() == 5
```

---

## Registry Tests

Test model registration, validation, and dynamic model creation.

```python
"""Tests for fairdm.registry."""

import pytest

from fairdm.core.sample.models import Sample
from fairdm.registry import registry
from fairdm.registry.config import ModelConfiguration


@pytest.mark.django_db
class TestModelRegistration:

    def test_register_valid_sample(self, clean_registry, unique_app_label):
        class TestSample(Sample):
            class Meta:
                app_label = unique_app_label

        class TestConfig(ModelConfiguration):
            model = TestSample
            fields = ["name"]

        clean_registry.register(TestConfig)

        assert clean_registry.is_registered(TestSample)

    def test_duplicate_registration_raises(self, clean_registry, unique_app_label):
        class TestSample(Sample):
            class Meta:
                app_label = unique_app_label

        class TestConfig(ModelConfiguration):
            model = TestSample
            fields = ["name"]

        clean_registry.register(TestConfig)

        with pytest.raises(Exception):
            clean_registry.register(TestConfig)

    def test_get_for_model_returns_config(self, clean_registry, unique_app_label):
        class TestSample(Sample):
            class Meta:
                app_label = unique_app_label

        class TestConfig(ModelConfiguration):
            model = TestSample
            fields = ["name"]

        clean_registry.register(TestConfig)
        config = clean_registry.get_for_model(TestSample)

        assert config.model is TestSample
```

### Key principles

- Always use `clean_registry` fixture — registry is shared global state.
- Always use `unique_app_label` for dynamic model `Meta.app_label`.
- `cleanup_test_app_models` runs autouse — no manual cleanup needed.

---

## Management Command Tests

```python
"""Tests for management commands."""

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestMyCommand:

    def test_command_runs_successfully(self, capsys):
        call_command("my_command", "--flag")

        captured = capsys.readouterr()
        assert "Success" in captured.out

    def test_command_with_invalid_args(self):
        with pytest.raises(SystemExit):
            call_command("my_command", "--invalid")
```

---

## Performance Guard Pattern

```python
@pytest.mark.django_db
def test_project_list_does_not_n_plus_one(client, django_assert_num_queries):
    """Verify list view uses constant queries regardless of row count."""
    ProjectFactory.create_batch(20)

    with django_assert_num_queries(3):  # adjust to actual count
        client.get(reverse("project-list"))
```

Never use `time.time()` or `timeit` for performance assertions.
