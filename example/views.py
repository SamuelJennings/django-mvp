"""Example views for demonstrating list and detail views."""

from django.views.generic import DetailView, ListView, TemplateView

from mvp.views import ListItemTemplateMixin, SearchOrderMixin

from .models import Article, Category, Product, Task


class ThemeTestView(TemplateView):
    """Demo view for testing custom theme with inner layout sidebars."""

    template_name = "demo/theme_test.html"


class HomeView(TemplateView):
    """Interactive home page with layout system demonstration.

    Provides an interactive demo of the layout system with real-time
    mode switching between navbar, sidebar, and both layouts.
    """

    template_name = "demo/home.html"


class ProductListView(ListItemTemplateMixin, SearchOrderMixin, ListView):
    """Product list view with various display options."""

    model = Product
    template_name = "example/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    # Search and order configuration
    search_fields = ["name", "description", "short_description", "sku", "tags"]
    order_by = [
        ("-created_at", "Newest First"),
        ("created_at", "Oldest First"),
        ("name", "Name A-Z"),
        ("-name", "Name Z-A"),
        ("price", "Price: Low to High"),
        ("-price", "Price: High to Low"),
        ("-rating", "Highest Rated"),
        ("stock", "Stock: Low to High"),
        ("-stock", "Stock: High to Low"),
    ]

    def get_queryset(self):
        """Get filtered queryset."""
        queryset = super().get_queryset().select_related("category")

        # Filter by category if provided
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by status
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Filter by availability
        available = self.request.GET.get("available")
        if available:
            queryset = queryset.filter(is_available=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        context["view_mode"] = self.request.GET.get("view", "grid")  # grid, list, table
        return context


class ProductDetailView(DetailView):
    """Product detail view."""

    model = Product
    template_name = "example/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        """Add related products."""
        context = super().get_context_data(**kwargs)
        context["related_products"] = Product.objects.filter(category=self.object.category, status="published").exclude(
            pk=self.object.pk
        )[:4]
        return context


class CategoryListView(ListItemTemplateMixin, SearchOrderMixin, ListView):
    """Category list view."""

    model = Category
    context_object_name = "categories"
    queryset = Category.objects.filter(is_active=True)

    # Search and order configuration
    search_fields = ["name", "description"]
    order_by = [
        ("name", "Name A-Z"),
        ("-name", "Name Z-A"),
        ("-created_at", "Newest First"),
        ("created_at", "Oldest First"),
    ]

    def get_context_data(self, **kwargs):
        """Add product counts."""
        context = super().get_context_data(**kwargs)
        for category in context["categories"]:
            category.product_count = category.products.filter(status="published").count()
        return context


class CategoryDetailView(DetailView):
    """Category detail view with products."""

    model = Category
    template_name = "example/category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        """Add category products."""
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.filter(status="published").select_related("category")[:12]
        return context


class ArticleListView(ListItemTemplateMixin, SearchOrderMixin, ListView):
    """Article list view."""

    model = Article
    template_name = "example/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    # Search and order configuration
    search_fields = ["title", "excerpt", "content", "author", "tags"]
    order_by = [
        ("-published_at", "Recently Published"),
        ("published_at", "Oldest Published"),
        ("-created_at", "Recently Created"),
        ("created_at", "Oldest Created"),
        ("title", "Title A-Z"),
        ("-title", "Title Z-A"),
        ("-views", "Most Viewed"),
        ("read_time", "Shortest Read"),
        ("-read_time", "Longest Read"),
    ]

    def get_queryset(self):
        """Get published articles."""
        queryset = super().get_queryset().select_related("category")

        # Filter by category
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by status
        status = self.request.GET.get("status", "published")
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        """Add categories."""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        return context


class ArticleDetailView(DetailView):
    """Article detail view."""

    model = Article
    template_name = "example/article_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        """Add related articles."""
        context = super().get_context_data(**kwargs)
        if self.object.category:
            context["related_articles"] = Article.objects.filter(
                category=self.object.category, status="published"
            ).exclude(pk=self.object.pk)[:3]
        else:
            context["related_articles"] = []
        return context


class TaskListView(ListItemTemplateMixin, SearchOrderMixin, ListView):
    """Task list view."""

    model = Task
    template_name = "example/task_list.html"
    context_object_name = "tasks"
    paginate_by = 20

    # Search and order configuration
    search_fields = ["title", "description", "assignee"]
    order_by = [
        ("due_date", "Due Date (Earliest)"),
        ("-due_date", "Due Date (Latest)"),
        ("-priority", "Priority (High to Low)"),
        ("priority", "Priority (Low to High)"),
        ("status", "Status"),
        ("-created_at", "Recently Created"),
        ("created_at", "Oldest First"),
        ("title", "Title A-Z"),
        ("-title", "Title Z-A"),
    ]

    def get_queryset(self):
        """Get filtered tasks."""
        queryset = super().get_queryset().select_related("category")

        # Filter by status
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Filter by priority
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        # Filter by assignee
        assignee = self.request.GET.get("assignee")
        if assignee:
            queryset = queryset.filter(assignee__icontains=assignee)

        return queryset

    def get_context_data(self, **kwargs):
        """Add task statistics."""
        context = super().get_context_data(**kwargs)
        all_tasks = Task.objects.all()
        context["stats"] = {
            "total": all_tasks.count(),
            "todo": all_tasks.filter(status="todo").count(),
            "in_progress": all_tasks.filter(status="in_progress").count(),
            "done": all_tasks.filter(status="done").count(),
        }
        return context


class TaskDetailView(DetailView):
    """Task detail view."""

    model = Task
    template_name = "example/task_detail.html"
    context_object_name = "task"
