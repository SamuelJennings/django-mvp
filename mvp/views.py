"""Views and view mixins for django-mvp."""

from django.db.models import Q
from django.views.generic import CreateView, FormView, UpdateView


class SearchMixin:
    """Mixin for handling search functionality on list views.

    This mixin provides search functionality similar to Django admin's
    search_fields, using the 'q' query parameter.

    Attributes:
        search_fields (list[str]): List of model field names to search across.
            Supports relationship lookups (e.g., 'descriptions__value').
            Default: None (no search).

    Example:
        class MyListView(SearchMixin, ListView):
            model = MyModel
            search_fields = ['name', 'description', 'related__field']

    Query Parameters:
        q (str): Search term to filter results across search_fields
    """

    search_fields = None

    def get_search_fields(self):
        """Return the list of fields to search across.

        Returns:
            list[str] or None: List of field names for search
        """
        return self.search_fields

    def get_queryset(self):
        """Apply search filtering to the queryset.

        Returns:
            QuerySet: Filtered queryset
        """
        queryset = super().get_queryset()

        # Apply search filtering
        search_term = self.request.GET.get("q", "").strip()
        if search_term and self.get_search_fields():
            queryset = self._apply_search(queryset, search_term)

        return queryset

    def _apply_search(self, queryset, search_term):
        """Apply search filtering across search_fields.

        Similar to Django admin's search functionality, this builds an OR query
        across all specified fields using case-insensitive contains lookups.
        For multi-word searches, applies OR matching across all words and fields.

        Args:
            queryset: The queryset to filter
            search_term: The search string (can contain multiple words)

        Returns:
            QuerySet: Filtered queryset
        """
        search_query = Q()

        # Split search term by any whitespace to support multi-word OR matching
        words = search_term.split()

        for word in words:
            for field in self.get_search_fields():
                search_query |= Q(**{f"{field}__icontains": word})

        return queryset.filter(search_query).distinct()

    def get_context_data(self, **kwargs):
        """Add search data to the template context.

        Adds:
            search_query (str): Current search term
        """
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["is_searchable"] = bool(self.search_fields)
        return context


class OrderMixin:
    """Mixin for handling ordering functionality on list views.

    This mixin provides ordering capabilities using the 'o' query parameter.

    Attributes:
        order_by (list[tuple[str, str]]): List of (ordering, label) tuples
            defining available ordering options. The ordering value should be
            a field name with optional '-' prefix for descending order.
            Default: None (no ordering).

    Example:
        class MyListView(OrderMixin, ListView):
            model = MyModel
            order_by = [
                ('name', 'Name A-Z'),
                ('-name', 'Name Z-A'),
                ('created', 'Oldest First'),
                ('-created', 'Newest First'),
            ]

    Query Parameters:
        o (str): Ordering value from the order_by choices
    """

    order_by = None

    def get_order_by_choices(self):
        """Return the list of ordering choices.

        Returns:
            list[tuple[str, str]] or None: List of (ordering, label) tuples
        """
        return self.order_by

    def get_queryset(self):
        """Apply ordering to the queryset.

        Returns:
            QuerySet: Ordered queryset
        """
        queryset = super().get_queryset()

        # Apply ordering
        ordering = self.request.GET.get("o", "")
        if ordering and self.get_order_by_choices():
            queryset = self._apply_ordering(queryset, ordering)

        return queryset

    def _apply_ordering(self, queryset, ordering):
        """Apply ordering to the queryset.

        Validates that the ordering value exists in the configured order_by
        choices before applying it to prevent arbitrary field ordering.

        Args:
            queryset: The queryset to order
            ordering: The ordering field name (with optional '-' prefix)

        Returns:
            QuerySet: Ordered queryset
        """
        # Validate ordering is in allowed choices
        valid_orderings = [choice[0] for choice in self.get_order_by_choices()]
        if ordering in valid_orderings:
            return queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        """Add ordering data to the template context.

        Adds:
            order_by_choices (list): Available ordering options
            current_ordering (str): Currently active ordering
        """
        context = super().get_context_data(**kwargs)

        # Add ordering context
        order_by_choices = self.get_order_by_choices()
        if order_by_choices:
            context["order_by_choices"] = order_by_choices
            context["current_ordering"] = self.request.GET.get("o", "")

        return context


class SearchOrderMixin(SearchMixin, OrderMixin):
    """Combined mixin for handling both search and ordering on list views.

    This mixin combines SearchMixin and OrderMixin to provide both search
    and ordering functionality using query parameters 'q' for search and 'o'
    for ordering.

    Attributes:
        search_fields (list[str]): List of model field names to search across.
            Supports relationship lookups (e.g., 'descriptions__value').
            Default: None (no search).
        order_by (list[tuple[str, str]]): List of (ordering, label) tuples
            defining available ordering options. The ordering value should be
            a field name with optional '-' prefix for descending order.
            Default: None (no ordering).

    Example:
        class MyListView(SearchOrderMixin, ListView):
            model = MyModel
            search_fields = ['name', 'description', 'related__field']
            order_by = [
                ('name', 'Name A-Z'),
                ('-name', 'Name Z-A'),
                ('created', 'Oldest First'),
                ('-created', 'Newest First'),
            ]

    Query Parameters:
        q (str): Search term to filter results across search_fields
        o (str): Ordering value from the order_by choices
    """

    pass


class ListItemTemplateMixin:
    """Mixin for providing list item template resolution for list views.

    This mixin automatically resolves the template to use for rendering
    individual list items in a list view. It follows Django's convention
    of app_label/model_name pattern.

    Attributes:
        list_item_template (str): Explicit template path for list items.
            If None, template is auto-generated via get_list_item_template().
            Default: None (auto-generate).

    Example:
        class MyListView(ListItemTemplateMixin, ListView):
            model = Product
            # Will automatically use: 'myapp/list_product_item.html'

        class CustomListView(ListItemTemplateMixin, ListView):
            model = Product
            list_item_template = 'custom/product_card.html'

        class OverrideListView(ListItemTemplateMixin, ListView):
            model = Product

            def get_list_item_template(self):
                # Custom logic for template selection
                if self.request.GET.get('compact'):
                    return 'myapp/compact_product_item.html'
                return 'myapp/full_product_item.html'

    Template Context:
        list_item_template (str): The resolved template path for list items
    """

    list_item_template = None

    def get_list_item_template(self):
        """Return the template path for rendering individual list items.

        If list_item_template is explicitly set, it is used.
        Otherwise, generates a template path following the pattern:
        '<app_label>/list_<model_name>_item.html'

        Returns:
            str: Template path for list item

        Raises:
            AttributeError: If model is not defined on the view
        """
        if self.list_item_template:
            return self.list_item_template

        # Auto-generate template name from model
        if not hasattr(self, "model") or self.model is None:
            msg = (
                f"{self.__class__.__name__} is missing a model. "
                "Define {0}.model or override "
                "{0}.get_list_item_template()."
            ).format(self.__class__.__name__)
            raise AttributeError(msg)

        opts = self.model._meta
        return f"{opts.app_label}/{opts.model_name}_list_item.html"

    def get_template_names(self):
        template_names = super().get_template_names()
        template_names.append("list_view.html")
        return template_names

    def get_context_data(self, **kwargs):
        """Add list item template to the template context.

        Adds:
            list_item_template (str): Template path for rendering list items
        """
        context = super().get_context_data(**kwargs)
        context["list_item_template"] = self.get_list_item_template()
        return context


class MVPListViewMixin(SearchOrderMixin, ListItemTemplateMixin):
    grid: dict = {}
    page_title = ""

    def get_context_data(self, **kwargs):
        """Add grid configuration to the template context.

        Adds:
            grid_config (GridConfig): Configuration for grid layout
        """
        context = super().get_context_data(**kwargs)
        context["grid_config"] = self.get_grid_config()
        context["page_title"] = self.get_page_title()
        return context

    def get_grid_config(self):
        return self.grid

    def get_page_title(self):
        if self.page_title:
            return self.page_title

        model = getattr(self, "model", None)
        if model:
            return model._meta.verbose_name_plural.title()

        return self.page_title


class PageModifierMixin:
    """Mixin for adding page modifier classes to the template context."""

    page = {}
    """Dictionary of page modifier classes that can be passed the the `c-page` component. """

    def get_context_data(self, **kwargs):
        """Add page modifier classes to the template context.

        Adds:
            page (dict): Dictionary of page modifier classes
        """
        context = super().get_context_data(**kwargs)
        context["page"] = self.page
        return context


def layout_demo(request):
    """Interactive layout demo page for testing AdminLTE layout configurations.

    Accepts query parameters to control layout options:
    - fixed_sidebar=on: Enable fixed sidebar (layout-fixed class)
    - fixed_header=on: Enable fixed header (fixed-header class)
    - fixed_footer=on: Enable fixed footer (fixed-footer class)
    - sidebar_expand=sm|md|lg|xl|xxl: Set sidebar expand breakpoint
    - sidebar_collapsible=on: Enable collapsible sidebar (sidebar-mini class)
    - collapsed=on: Start with sidebar collapsed (sidebar-collapse class)

    Returns:
        HttpResponse: Rendered layout demo page with form controls and layout preview
    """
    from django.shortcuts import render

    # Parse query parameters for layout configuration
    layout_config = {
        "fixed_sidebar": request.GET.get("fixed_sidebar") == "on",
        "fixed_header": request.GET.get("fixed_header") == "on",
        "fixed_footer": request.GET.get("fixed_footer") == "on",
        "sidebar_collapsible": request.GET.get("sidebar_collapsible") == "on",
        "collapsed": request.GET.get("collapsed") == "on",
    }

    # Handle sidebar expand with validation and fallback
    sidebar_expand = request.GET.get("sidebar_expand", "lg")
    valid_breakpoints = ["sm", "md", "lg", "xl", "xxl"]
    if sidebar_expand not in valid_breakpoints:
        sidebar_expand = "lg"  # Fallback to default
    layout_config["sidebar_expand"] = sidebar_expand

    context = {
        "layout_config": layout_config,
        "valid_breakpoints": valid_breakpoints,
        "page_title": "Interactive Layout Demo",
        "breadcrumb": "Layout Configuration Demo",
    }

    return render(request, "mvp/layout_demo.html", context)


class MVPFormViewMixin:
    """Mixin to render forms in AdminLTE layout with auto-detected renderer.

    This mixin provides automatic form renderer detection and a consistent
    AdminLTE card-based layout for form views. It detects django-crispy-forms,
    django-formset, or falls back to standard Django form rendering.

    Attributes:
        form_renderer (str|None): Override renderer ("crispy", "formset", "django").
            None enables auto-detection (default).
        page_title (str): Title displayed in the form card header.
        template_name (str): Template path for form rendering.

    Priority Order (auto-detection):
        1. django-crispy-forms (if installed)
        2. django-formset (if installed)
        3. Standard Django form.as_p (fallback)

    Example:
        class ContactView(MVPFormViewMixin, FormView):
            form_class = ContactForm
            success_url = "/thanks/"
            page_title = "Contact Us"
            form_renderer = "crispy"  # Optional explicit override
    """

    form_renderer = None  # None = auto-detect, or "crispy", "formset", "django"
    page_title = ""
    template_name = "mvp/form_view.html"

    def get_form_renderer(self):
        """Determine which form renderer to use.

        Returns:
            str: Renderer name ("crispy", "formset", or "django")

        Logic:
            1. If form_renderer is explicitly set, validate and use it
            2. Otherwise, auto-detect based on installed apps:
               - crispy_forms (highest priority)
               - formset (second priority)
               - django (fallback)
            3. Log warning if explicit renderer is not available
        """
        import logging

        from mvp.utils import app_is_installed

        logger = logging.getLogger(__name__)

        # Explicit renderer override
        if self.form_renderer:
            # Validate explicit renderer is available
            if self.form_renderer == "crispy" and not app_is_installed("crispy_forms"):
                logger.warning(
                    "MVPFormViewMixin: form_renderer='crispy' but django-crispy-forms "
                    "is not installed. Falling back to django renderer."
                )
                return "django"
            if self.form_renderer == "formset" and not app_is_installed("formset"):
                logger.warning(
                    "MVPFormViewMixin: form_renderer='formset' but django-formset "
                    "is not installed. Falling back to django renderer."
                )
                return "django"
            return self.form_renderer

        # Auto-detection priority: crispy → formset → django
        if app_is_installed("crispy_forms"):
            return "crispy"
        if app_is_installed("formset"):
            return "formset"
        return "django"

    def get_page_title(self):
        """Return the page title for the form.

        Returns:
            str: Page title from page_title attribute
        """
        return self.page_title

    def get_context_data(self, **kwargs):
        """Inject form renderer and page title into template context.

        Returns:
            dict: Context with form_renderer and page_title added
        """
        context = super().get_context_data(**kwargs)
        context["form_renderer"] = self.get_form_renderer()
        context["page_title"] = self.get_page_title()
        return context


class MVPFormView(MVPFormViewMixin, FormView):
    """FormView with AdminLTE layout and auto-detected form rendering.

    Combines MVPFormViewMixin with Django's FormView to provide a complete
    form view with automatic renderer detection and AdminLTE card layout.

    Inherits all attributes and methods from MVPFormViewMixin and FormView.

    Example:
        class ContactView(MVPFormView):
            form_class = ContactForm
            success_url = "/contact/success/"
            page_title = "Contact Us"
    """

    pass


class MVPCreateView(MVPFormViewMixin, CreateView):
    """CreateView with AdminLTE layout and auto-detected form rendering.

    Combines MVPFormViewMixin with Django's CreateView to provide a model
    form create view with automatic renderer detection and AdminLTE card layout.

    Inherits all attributes and methods from MVPFormViewMixin and CreateView.

    Attributes:
        model (Model): The model class for the form (inherited from CreateView)
        fields (list[str]): List of model fields to include in form (inherited from CreateView)
        form_class (Form): Optional custom form class (inherited from CreateView)
        success_url (str): URL to redirect to after successful form submission

    Example:
        class ProductCreateView(MVPCreateView):
            model = Product
            fields = ['name', 'price', 'description']
            success_url = "/products/"
            page_title = "Add New Product"

        # Or with custom form:
        class ProductCreateView(MVPCreateView):
            model = Product
            form_class = ProductForm
            success_url = "/products/"
            page_title = "Add New Product"
    """

    pass


class MVPUpdateView(MVPFormViewMixin, UpdateView):
    """UpdateView with AdminLTE layout and auto-detected form rendering.

    Combines MVPFormViewMixin with Django's UpdateView to provide a model
    form edit view with automatic renderer detection and AdminLTE card layout.

    Inherits all attributes and methods from MVPFormViewMixin and UpdateView.

    Attributes:
        model (Model): The model class for the form (inherited from UpdateView)
        fields (list[str]): List of model fields to include in form (inherited from UpdateView)
        form_class (Form): Optional custom form class (inherited from UpdateView)
        success_url (str): URL to redirect to after successful form submission
        pk_url_kwarg (str): URL keyword argument for primary key (default: 'pk')
        slug_url_kwarg (str): URL keyword argument for slug (default: 'slug')

    Example:
        # In urls.py:
        path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit')

        # View class:
        class ProductUpdateView(MVPUpdateView):
            model = Product
            fields = ['name', 'price', 'description']
            success_url = "/products/"
            page_title = "Edit Product"

        # Or with custom form:
        class ProductUpdateView(MVPUpdateView):
            model = Product
            form_class = ProductForm
            success_url = "/products/"
            page_title = "Edit Product"
    """

    pass
