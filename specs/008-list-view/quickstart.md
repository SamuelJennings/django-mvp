# Quickstart: Dashboard List View Mixin

**Feature**: 008-dash-list-view
**Date**: February 4, 2026

## Minimal Example (10 lines)

Create a fully functional list view with just a model and template:

```python
# views.py
from django.views.generic import ListView
from mvp.views import MVPListViewMixin

class ProductListView(MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
```

That's it! You get:

- ✅ Page title from model's `verbose_name_plural`
- ✅ Single-column grid layout
- ✅ Pagination with entry counts
- ✅ Empty state handling

## Add Search

Enable search by specifying fields to search across:

```python
class ProductListView(MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
    search_fields = ["name", "description", "sku"]  # ← Add this
```

Users can now search via the search bar in the page header. Multi-word searches use OR matching.

## Add Ordering

Enable sorting with labeled options:

```python
class ProductListView(MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
    search_fields = ["name", "description"]
    order_by = [                                    # ← Add this
        ("name", "Name (A-Z)"),
        ("-name", "Name (Z-A)"),
        ("price", "Price (Low to High)"),
        ("-price", "Price (High to Low)"),
    ]
```

A sort dropdown appears in the page header. Use `-` prefix for descending order.

## Configure Grid Layout

Customize the grid with responsive breakpoints:

```python
class ProductListView(MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
    grid = {                                        # ← Add this
        "cols": 1,      # Default: 1 column
        "md": 2,        # 2 columns on tablets (≥768px)
        "lg": 3,        # 3 columns on desktops (≥992px)
        "gap": 2,       # Gap between items
    }
```

Grid options: `cols`, `xs`, `sm`, `md`, `lg`, `xl`, `xxl`, `gap`

## Add Filtering (django-filter)

For advanced filtering, use `FilterView` with django-filter:

```python
from django_filters.views import FilterView
from mvp.views import MVPListViewMixin

class ProductListView(MVPListViewMixin, FilterView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
    filterset_fields = ["category", "status"]       # ← django-filter
    search_fields = ["name", "description"]
    order_by = [("name", "Name"), ("-price", "Price")]
```

A filter toggle button appears in the page header. Click to open the filter sidebar.

## Override with Methods

All attributes can be overridden with methods for dynamic behavior:

```python
class ProductListView(MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"

    def get_page_title(self):
        """Dynamic page title based on category."""
        category = self.request.GET.get("category")
        if category:
            return f"{category} Products"
        return "All Products"

    def get_search_fields(self):
        """Conditionally enable search."""
        if self.request.user.has_perm("myapp.can_search"):
            return ["name", "description", "sku"]
        return None

    def get_grid_config(self):
        """Responsive grid based on user preference."""
        if self.request.GET.get("compact"):
            return {"cols": 1, "md": 3, "lg": 4, "gap": 1}
        return {"cols": 1, "md": 2, "lg": 3, "gap": 2}
```

## List Item Template

Create a template for rendering each item. It receives `object` in context:

```django
{# myapp/product_card.html #}
<c-card title="{{ object.name }}">
    <p>{{ object.description|truncatewords:30 }}</p>
    <p class="fw-bold">${{ object.price }}</p>
</c-card>
```

Or auto-generate the template path based on model:

```python
class ProductListView(MVPListViewMixin, ListView):
    model = Product  # Auto-uses: myapp/product_list_item.html
    template_name = "mvp/list_view.html"
```

## URL Configuration

```python
# urls.py
from django.urls import path
from .views import ProductListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
]
```

## Full Example

```python
from django.views.generic import ListView
from mvp.views import MVPListViewMixin, PageModifierMixin

class ProductListView(PageModifierMixin, MVPListViewMixin, ListView):
    model = Product
    template_name = "mvp/list_view.html"
    list_item_template = "myapp/product_card.html"
    paginate_by = 12
    page = {"layout": "ts-ms-ff"}                   # Page layout
    grid = {"cols": 1, "md": 2, "xl": 3, "gap": 2}  # Responsive grid
    search_fields = ["name", "description", "sku"]  # Searchable fields
    order_by = [                                     # Sort options
        ("name", "Name (A-Z)"),
        ("-name", "Name (Z-A)"),
        ("-created_at", "Newest First"),
        ("price", "Price (Low to High)"),
    ]
```

## Mixin Reference

| Mixin | Purpose | Key Attributes |
|-------|---------|----------------|
| `SearchMixin` | Search functionality | `search_fields` |
| `OrderMixin` | Ordering/sorting | `order_by` |
| `SearchOrderMixin` | Combined search + order | (inherits both) |
| `ListItemTemplateMixin` | List item rendering | `list_item_template` |
| `MVPListViewMixin` | Full feature set | `grid`, `page_title` |

Use `MVPListViewMixin` for the complete package, or individual mixins for specific needs.
