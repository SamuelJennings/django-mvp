"""Tests for list view mixins."""

import pytest
from django.test import RequestFactory
from django.views.generic import ListView

from example.models import Product
from mvp.views import (
    ListItemTemplateMixin,
    MVPListViewMixin,
    OrderMixin,
    SearchMixin,
    SearchOrderMixin,
)


@pytest.fixture
def request_factory():
    """Provide Django request factory."""
    return RequestFactory()


@pytest.fixture
def sample_products(db):
    """Create sample products for testing."""
    from example.models import Category

    # Create test category
    category = Category.objects.create(
        name="Test Category",
        slug="test-category",
        description="Test category for products",
    )

    # Create test products with various attributes
    products = [
        Product.objects.create(
            name="Red Car Model",
            slug="red-car",
            category=category,
            description="A beautiful red sports car",
            short_description="Red sports car",
            price=50000.00,
            stock=5,
            status="published",
            sku="RC001",
        ),
        Product.objects.create(
            name="Blue Bicycle",
            slug="blue-bike",
            category=category,
            description="A comfortable blue bicycle for city rides",
            short_description="Blue city bicycle",
            price=500.00,
            stock=10,
            status="published",
            sku="BB001",
        ),
        Product.objects.create(
            name="Green Car Toy",
            slug="green-car-toy",
            category=category,
            description="A small green toy car for children",
            short_description="Green toy car",
            price=20.00,
            stock=50,
            status="published",
            sku="GT001",
        ),
        Product.objects.create(
            name="Yellow Scooter",
            slug="yellow-scooter",
            category=category,
            description="A fast yellow electric scooter",
            short_description="Yellow electric scooter",
            price=800.00,
            stock=8,
            status="published",
            sku="YS001",
        ),
    ]

    return products


class TestSearchMixin:
    """Tests for SearchMixin functionality."""

    class TestView(SearchMixin, ListView):
        """Test view using SearchMixin."""

        model = Product
        search_fields = ["name", "description"]

    def test_single_word_search(self, request_factory, sample_products):
        """Test single-word search matches correctly."""
        # Test searching for "car" - should match "Red Car Model" and "Green Car Toy"
        request = request_factory.get("/?q=car")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]

        assert len(results) == 2
        assert "Red Car Model" in result_names
        assert "Green Car Toy" in result_names

    def test_multi_word_or_search(self, request_factory, sample_products):
        """Test multi-word search uses OR matching across words (FR-020).

        This is the critical test for T005 - verifying that searching for
        "red car" matches records containing "red" OR "car", not just the
        exact phrase "red car".
        """
        # Test searching for "red car" - should match:
        # - "Red Car Model" (contains both "red" and "car")
        # - "Green Car Toy" (contains "car")
        # But NOT:
        # - "Blue Bicycle" (contains neither)
        # - "Yellow Scooter" (contains neither)
        request = request_factory.get("/?q=red car")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]

        assert len(results) == 2, f"Expected 2 results, got {len(results)}: {result_names}"
        assert "Red Car Model" in result_names
        assert "Green Car Toy" in result_names
        assert "Blue Bicycle" not in result_names
        assert "Yellow Scooter" not in result_names

    def test_multi_word_or_search_multiple_fields(self, request_factory, sample_products):
        """Test multi-word search works across multiple fields."""
        # Test searching for "blue city" - should match:
        # - "Blue Bicycle" (name contains "blue", description contains "city")
        request = request_factory.get("/?q=blue city")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]

        assert len(results) == 1
        assert "Blue Bicycle" in result_names

    def test_empty_search(self, request_factory, sample_products):
        """Test empty search returns all results."""
        request = request_factory.get("/?q=")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        assert len(results) == 4

    def test_no_search_parameter(self, request_factory, sample_products):
        """Test missing search parameter returns all results."""
        request = request_factory.get("/")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        assert len(results) == 4

    def test_search_with_whitespace_variations(self, request_factory, sample_products):
        """Test search handles multiple spaces, tabs, newlines."""
        # Test with multiple spaces
        request = request_factory.get("/?q=red  car")  # Two spaces
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]

        assert len(results) == 2
        assert "Red Car Model" in result_names
        assert "Green Car Toy" in result_names

    def test_search_context_variables(self, request_factory, sample_products):
        """Test search adds correct context variables."""
        request = request_factory.get("/?q=test search")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        assert context["search_query"] == "test search"
        assert context["is_searchable"] is True

    def test_get_search_fields(self, request_factory):
        """Test get_search_fields returns configured fields."""
        view = self.TestView()
        view.request = request_factory.get("/")

        fields = view.get_search_fields()

        assert fields == ["name", "description"]


@pytest.mark.django_db
class TestOrderMixin:
    """Tests for OrderMixin functionality (T056)."""

    class TestView(OrderMixin, ListView):
        """Test view using OrderMixin."""

        model = Product
        order_by = [
            ("name", "Name (A-Z)"),
            ("-name", "Name (Z-A)"),
            ("price", "Price (Low to High)"),
            ("-price", "Price (High to Low)"),
        ]

    def test_get_order_by_choices(self, request_factory):
        """Test get_order_by_choices returns configured ordering options."""
        view = self.TestView()
        view.request = request_factory.get("/")

        choices = view.get_order_by_choices()

        assert len(choices) == 4
        assert choices == [
            ("name", "Name (A-Z)"),
            ("-name", "Name (Z-A)"),
            ("price", "Price (Low to High)"),
            ("-price", "Price (High to Low)"),
        ]

    def test_apply_ordering_ascending(self, request_factory, sample_products):
        """Test ordering applies correctly in ascending order."""
        request = request_factory.get("/?o=name")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]

        # Should be alphabetically ordered
        assert result_names == sorted(result_names)
        assert result_names[0] == "Blue Bicycle"

    def test_apply_ordering_descending(self, request_factory, sample_products):
        """Test ordering applies correctly in descending order."""
        request = request_factory.get("/?o=-price")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        prices = [p.price for p in results]

        # Should be reverse ordered by price
        assert prices == sorted(prices, reverse=True)
        assert prices[0] == 50000.00  # Red Car Model

    def test_ordering_context_variables(self, request_factory, sample_products):
        """Test ordering adds correct context variables."""
        request = request_factory.get("/?o=price")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        assert "order_by_choices" in context
        assert context["order_by_choices"] == view.order_by
        assert context["current_ordering"] == "price"

    def test_invalid_ordering_ignored(self, request_factory, sample_products):
        """Test invalid ordering parameter is ignored."""
        request = request_factory.get("/?o=invalid_field")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)

        # Should return results in default order (no error)
        assert len(results) == 4

    def test_no_ordering_parameter(self, request_factory, sample_products):
        """Test missing ordering parameter returns results in default order."""
        request = request_factory.get("/")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        assert len(results) == 4


@pytest.mark.django_db
class TestSearchOrderMixin:
    """Tests for combined SearchOrderMixin functionality (T057)."""

    class TestView(SearchOrderMixin, ListView):
        """Test view using SearchOrderMixin."""

        model = Product
        search_fields = ["name", "description"]
        order_by = [
            ("name", "Name (A-Z)"),
            ("price", "Price (Low to High)"),
        ]

    def test_search_and_order_combined(self, request_factory, sample_products):
        """Test search and ordering work together correctly."""
        # Search for "car" and order by price
        request = request_factory.get("/?q=car&o=price")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        results = list(view.object_list)
        result_names = [p.name for p in results]
        prices = [p.price for p in results]

        # Should only include results with "car"
        assert len(results) == 2
        assert "Red Car Model" in result_names
        assert "Green Car Toy" in result_names

        # And should be ordered by price
        assert prices == sorted(prices)
        assert prices[0] == 20.00  # Green Car Toy
        assert prices[1] == 50000.00  # Red Car Model

    def test_combined_functionality_context(self, request_factory, sample_products):
        """Test combined mixin provides all context variables."""
        request = request_factory.get("/?q=test&o=name")
        view = self.TestView()
        view.request = request
        view.kwargs = {}
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        # Should have both search and ordering context
        assert context["search_query"] == "test"
        assert context["is_searchable"] is True
        assert "order_by_choices" in context
        assert context["current_ordering"] == "name"


@pytest.mark.django_db
class TestListItemTemplateMixin:
    """Tests for ListItemTemplateMixin functionality (T058)."""

    class TestView(ListItemTemplateMixin, ListView):
        """Test view using ListItemTemplateMixin."""

        model = Product
        list_item_template = "cards/product_card.html"

    def test_list_item_template_attribute(self, request_factory):
        """Test list_item_template attribute is set correctly."""
        view = self.TestView()
        view.request = request_factory.get("/")

        assert view.list_item_template == "cards/product_card.html"

    def test_get_list_item_template(self, request_factory):
        """Test get_list_item_template returns configured template."""
        view = self.TestView()
        view.request = request_factory.get("/")

        template = view.get_list_item_template()

        assert template == "cards/product_card.html"

    def test_get_list_item_template_override(self, request_factory):
        """Test get_list_item_template can be overridden."""

        class CustomView(ListItemTemplateMixin, ListView):
            model = Product
            list_item_template = "default.html"

            def get_list_item_template(self):
                return "custom.html"

        view = CustomView()
        view.request = request_factory.get("/")

        template = view.get_list_item_template()
        assert template == "custom.html"

    def test_template_context_variable(self, request_factory, sample_products):
        """Test list_item_template is added to context."""
        view = self.TestView()
        view.request = request_factory.get("/")
        view.kwargs = {}
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        assert context["list_item_template"] == "cards/product_card.html"


@pytest.mark.django_db
class TestMVPListViewMixin:
    """Tests for MVPListViewMixin functionality (T059)."""

    class TestView(MVPListViewMixin, ListView):
        """Test view using MVPListViewMixin."""

        model = Product
        grid = {"cols": 1, "md": 2, "lg": 3}

    def test_grid_config(self, request_factory):
        """Test grid configuration is set correctly."""
        view = self.TestView()
        view.request = request_factory.get("/")

        assert view.grid == {"cols": 1, "md": 2, "lg": 3}

    def test_get_grid_config(self, request_factory):
        """Test get_grid_config returns configured grid."""
        view = self.TestView()
        view.request = request_factory.get("/")

        config = view.get_grid_config()

        assert config == {"cols": 1, "md": 2, "lg": 3}

    def test_grid_config_default(self, request_factory):
        """Test default grid configuration when not specified."""

        class DefaultView(MVPListViewMixin, ListView):
            model = Product

        view = DefaultView()
        view.request = request_factory.get("/")

        config = view.get_grid_config()

        # Should default to empty dict (template will apply single column)
        assert config == {}

    def test_page_title_from_model(self, request_factory):
        """Test page title is derived from model verbose_name_plural."""
        view = self.TestView()
        view.request = request_factory.get("/")

        title = view.get_page_title()

        assert title == "Products"  # From Product model verbose_name_plural

    def test_get_page_title_override(self, request_factory):
        """Test get_page_title can be overridden."""

        class CustomView(MVPListViewMixin, ListView):
            model = Product

            def get_page_title(self):
                return "Custom Title"

        view = CustomView()
        view.request = request_factory.get("/")

        title = view.get_page_title()
        assert title == "Custom Title"

    def test_context_variables(self, request_factory, sample_products):
        """Test MVP mixin adds correct context variables."""
        view = self.TestView()
        view.request = request_factory.get("/")
        view.kwargs = {}
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        assert context["page_title"] == "Products"
        assert context["grid_config"] == {"cols": 1, "md": 2, "lg": 3}

