# Data Model: Form View Mixin

**Feature**: 009-form-view-mixin
**Date**: June 2025

## Mixin Class Hierarchy

```text
                   ┌─────────────────────┐
                   │  MVPFormViewMixin    │
                   │                     │
                   │ form_renderer       │
                   │ page_title          │
                   │ template_name       │
                   │ get_form_renderer() │
                   │ get_page_title()    │
                   │ get_context_data()  │
                   └──────────┬──────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌──────────────────────┐
    │   MVPFormView   │             │  MVPModelFormView    │
    │                 │             │                      │
    │ (MVPFormViewMixin │           │ (MVPFormViewMixin    │
    │  + FormView)    │             │  + CreateView)       │
    └─────────────────┘             └──────────────────────┘
```

## Entity Definitions

### MVPFormViewMixin

**Purpose**: Adds renderer detection, page title, and AdminLTE form layout to any Django form-based CBV.

**Attributes**:

| Attribute       | Type         | Default               | Description                                          |
| --------------- | ------------ | --------------------- | ---------------------------------------------------- |
| `form_renderer` | `str | None` | `None`                | Form rendering backend: `None` (auto), `"crispy"`, `"formset"`, or `"django"` |
| `page_title`    | `str`        | `""`                  | Page title displayed in card header                  |
| `template_name` | `str`        | `"mvp/form_view.html"`| Default template with conditional rendering          |

**Methods**:

| Method               | Returns  | Description                                                    |
| -------------------- | -------- | -------------------------------------------------------------- |
| `get_form_renderer()` | `str`   | Resolves renderer: explicit → auto-detect → fallback           |
| `get_page_title()`    | `str`   | Returns `page_title` attribute (can be overridden)             |
| `get_context_data()`  | `dict`  | Adds `page_title`, `form_renderer` to template context         |

**Context Variables Injected**:

| Variable        | Type   | Description                                         |
| --------------- | ------ | --------------------------------------------------- |
| `page_title`    | `str`  | Title for the form card header                      |
| `form_renderer` | `str`  | Resolved renderer name: `"crispy"`, `"formset"`, or `"django"` |
| `form`          | `Form` | Django form instance (from parent CBV)              |

### MVPFormView

**Purpose**: Pre-composed view combining `MVPFormViewMixin` with Django's `FormView` for plain forms.

**Inherits**: `MVPFormViewMixin`, `django.views.generic.FormView`

**Additional Attributes**: None (inherits from both parents)

**Additional Methods**: None

**Usage Pattern**:

```python
from mvp.views import MVPFormView

class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"
```

### MVPCreateView

**Purpose**: Pre-composed view combining `MVPFormViewMixin` with Django's `CreateView` for creating new model records.

**Inherits**: `MVPFormViewMixin`, `django.views.generic.CreateView`

**Additional Attributes**: None (inherits from both parents)

**Additional Methods**: None

**Usage Pattern**:

```python
from mvp.views import MVPCreateView

class ProductCreateView(MVPCreateView):
    model = Product
    fields = ["name", "price", "description"]
    success_url = "/products/"
    page_title = "Add Product"
```

### MVPUpdateView

**Purpose**: Pre-composed view combining `MVPFormViewMixin` with Django's `UpdateView` for editing existing model records.

**Inherits**: `MVPFormViewMixin`, `django.views.generic.UpdateView`

**Additional Attributes**: None (inherits from both parents)

**Additional Methods**: None

**Usage Pattern**:

```python
from mvp.views import MVPUpdateView

class ProductUpdateView(MVPUpdateView):
    model = Product
    fields = ["name", "price", "description"]
    success_url = "/products/"
    page_title = "Edit Product"
```

## Renderer Detection Logic

### `get_form_renderer()` Decision Tree

```text
Input: self.form_renderer (class attribute or .as_view() override)

1. If form_renderer is explicitly set:
   a. Validate renderer name is one of: "crispy", "formset", "django"
   b. Check if corresponding library is installed:
      - "crispy" → app_is_installed("crispy_forms")
      - "formset" → app_is_installed("formset")
      - "django" → always available
   c. If installed → return form_renderer
   d. If NOT installed → log warning, return "django"

2. If form_renderer is None (auto-detect):
   a. If app_is_installed("crispy_forms") → return "crispy"
   b. If app_is_installed("formset") → return "formset"
   c. return "django"
```

### Renderer-to-Library Mapping

| Renderer Value | Django App Name   | Template Tag                                       |
| -------------- | ----------------- | -------------------------------------------------- |
| `"crispy"`     | `crispy_forms`    | `{% load crispy_forms_tags %}{% crispy form %}`     |
| `"formset"`    | `formset`         | `{% load formsetify %}{% render_form form "bootstrap" %}` |
| `"django"`     | (built-in)        | `{{ form.as_p }}` with manual error display         |

## Template Contract

### `mvp/form_view.html`

**Expects Context**:

| Variable        | Type   | Required | Source                   |
| --------------- | ------ | -------- | ------------------------ |
| `page_title`    | `str`  | Yes      | `MVPFormViewMixin`       |
| `form_renderer` | `str`  | Yes      | `MVPFormViewMixin`       |
| `form`          | `Form` | Yes      | Django's `FormView`/`CreateView` |

**Renders**:

- AdminLTE card layout with header (title), body (form), footer (submit)
- Conditional form rendering based on `form_renderer` value
- Non-field error summary at top for all renderers
- Inline field errors (automatic for crispy/formset; manual for django)

### Template Block Structure

```text
{% extends "mvp/base.html" %}

{% block content %}
  <c-page title="{{ page_title }}">
    <c-page.content>
      <form method="post">
        {% csrf_token %}
        <c-card title="{{ page_title }}">
          <!-- Non-field errors (all renderers) -->
          <!-- Conditional form body based on form_renderer -->
          <c-slot name="footer_end">
            <button type="submit" class="btn btn-primary">Save</button>
          </c-slot>
        </c-card>
      </form>
    </c-page.content>
  </c-page>
{% endblock %}
```

## Validation Rules

| Rule | Scope | Description |
| ---- | ----- | ----------- |
| VR-001 | `form_renderer` | Must be `None`, `"crispy"`, `"formset"`, or `"django"` |
| VR-002 | Fallback | Invalid/unavailable renderer → log warning + use `"django"` |
| VR-003 | `page_title` | Empty string allowed (card renders without header) |
| VR-004 | `form` | Must be a valid Django `Form` or `ModelForm` instance |

## State Transitions

Not applicable — the mixin is stateless. Form processing (valid/invalid) is handled by Django's standard `FormView` / `CreateView` lifecycle.
