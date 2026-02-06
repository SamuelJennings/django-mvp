# Quickstart: Form View Mixin

**Feature**: 009-form-view-mixin
**Date**: June 2025

## Minimal Example — Plain Form

Create a fully functional form view with just a form class and success URL:

```python
# views.py
from django import forms
from mvp.views import MVPFormView


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"
```

That's it! You get:

- ✅ Auto-detected form renderer (crispy-forms → django-formset → standard Django)
- ✅ AdminLTE card layout with title, form body, and submit button
- ✅ Non-field error summary + inline field errors
- ✅ CSRF protection

## Minimal Example — Creating Model Records

Create a model form view for creating new objects:

```python
# views.py
from mvp.views import MVPCreateView
from myapp.models import Product


class ProductCreateView(MVPCreateView):
    model = Product
    fields = ["name", "price", "description"]
    success_url = "/products/"
    page_title = "Add Product"
```

## Minimal Example — Editing Model Records

Create a model form view for editing existing objects:

```python
# views.py
from mvp.views import MVPUpdateView
from myapp.models import Product


class ProductUpdateView(MVPUpdateView):
    model = Product
    fields = ["name", "price", "description"]
    success_url = "/products/"
    page_title = "Edit Product"
```

Wire up in `urls.py`:

```python
from django.urls import path
from myapp.views import ContactView, ProductCreateView, ProductUpdateView

urlpatterns = [
    path("contact/", ContactView.as_view(), name="contact"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
]
```

## Force a Specific Renderer

Override the auto-detected renderer with the `form_renderer` attribute:

```python
class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"
    form_renderer = "django"  # ← Force standard Django rendering
```

Valid values: `"crispy"`, `"formset"`, `"django"`, or `None` (auto-detect).

## Override via `.as_view()`

Use Django's standard `.as_view()` pattern to override attributes in URL config:

```python
# urls.py
urlpatterns = [
    path(
        "contact/",
        ContactView.as_view(form_renderer="crispy", page_title="Get in Touch"),
        name="contact",
    ),
]
```

## Customize the Template

Override `template_name` to use your own template:

```python
class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"
    template_name = "myapp/contact_form.html"  # ← Custom template
```

Your custom template receives these context variables:

| Variable        | Type   | Description                                    |
| --------------- | ------ | ---------------------------------------------- |
| `form`          | `Form` | The Django form instance                       |
| `page_title`    | `str`  | Title for the page/card header                 |
| `form_renderer` | `str`  | Resolved renderer: `"crispy"`, `"formset"`, or `"django"` |

## Handle Form Submission

Override `form_valid()` to customize success behavior (standard Django pattern):

```python
from django.contrib import messages

class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"

    def form_valid(self, form):
        # Process form data
        send_email(form.cleaned_data)
        messages.success(self.request, "Message sent!")
        return super().form_valid(form)
```

## Comparison: Before and After

### Before (Manual Setup)

```python
# views.py — 20+ lines
from django.views.generic import FormView

class ContactView(FormView):
    form_class = ContactForm
    template_name = "myapp/contact.html"
    success_url = "/thanks/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contact Us"
        return context
```

```html
<!-- myapp/contact.html — 15+ lines -->
{% extends "mvp/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div class="card">
  <div class="card-header"><h3>Contact Us</h3></div>
  <div class="card-body">
    <form method="post">
      {% csrf_token %}
      {% crispy form %}
      <button type="submit" class="btn btn-primary">Send</button>
    </form>
  </div>
</div>
{% endblock %}
```

### After (With MVPFormView / MVPCreateView / MVPUpdateView)

```python
# views.py — 5 lines
from mvp.views import MVPFormView

class ContactView(MVPFormView):
    form_class = ContactForm
    success_url = "/thanks/"
    page_title = "Contact Us"
```

No custom template needed — the default `mvp/form_view.html` handles everything.
