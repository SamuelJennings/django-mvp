"""Tests for ListItemTemplateMixin."""

import pytest
from django.test import RequestFactory
from django.views.generic import ListView

from example.models import Article, Category, Product
from mvp.views import ListItemTemplateMixin


class TestListItemTemplateMixin:
    """Test suite for ListItemTemplateMixin."""

    @pytest.fixture
    def request_factory(self):
        """Return a RequestFactory instance."""
        return RequestFactory()

    @pytest.mark.django_db
    def test_auto_generated_template_name(self, request_factory):
        """Test that template name is auto-generated from model."""

        class ProductListView(ListItemTemplateMixin, ListView):
            model = Product

        view = ProductListView()
        view.request = request_factory.get("/")
        view.object_list = Product.objects.none()

        template_name = view.get_list_item_template()

        assert template_name == "example/list_product_item.html"

    @pytest.mark.django_db
    def test_auto_generated_template_name_different_model(self, request_factory):
        """Test template name auto-generation with different model."""

        class CategoryListView(ListItemTemplateMixin, ListView):
            model = Category

        view = CategoryListView()
        view.request = request_factory.get("/")
        view.object_list = Category.objects.none()

        template_name = view.get_list_item_template()

        assert template_name == "example/list_category_item.html"

    @pytest.mark.django_db
    def test_explicit_list_item_template(self, request_factory):
        """Test that explicit list_item_template is used when set."""

        class ProductListView(ListItemTemplateMixin, ListView):
            model = Product
            list_item_template = "custom/product_card.html"

        view = ProductListView()
        view.request = request_factory.get("/")
        view.object_list = Product.objects.none()

        template_name = view.get_list_item_template()

        assert template_name == "custom/product_card.html"

    @pytest.mark.django_db
    def test_override_get_list_item_template(self, request_factory):
        """Test that get_list_item_template can be overridden."""

        class ProductListView(ListItemTemplateMixin, ListView):
            model = Product

            def get_list_item_template(self):
                if self.request.GET.get("compact"):
                    return "example/compact_product_item.html"
                return "example/full_product_item.html"

        # Test without compact parameter
        view = ProductListView()
        view.request = request_factory.get("/")
        view.object_list = Product.objects.none()

        template_name = view.get_list_item_template()
        assert template_name == "example/full_product_item.html"

        # Test with compact parameter
        view.request = request_factory.get("/?compact=1")
        template_name = view.get_list_item_template()
        assert template_name == "example/compact_product_item.html"

    @pytest.mark.django_db
    def test_context_data_includes_template(self, request_factory):
        """Test that list_item_template is added to context."""

        class ProductListView(ListItemTemplateMixin, ListView):
            model = Product

        view = ProductListView()
        view.request = request_factory.get("/")
        view.object_list = Product.objects.none()

        context = view.get_context_data()

        assert "list_item_template" in context
        assert context["list_item_template"] == "example/list_product_item.html"

    @pytest.mark.django_db
    def test_missing_model_raises_error(self, request_factory):
        """Test that missing model raises AttributeError."""

        class BadListView(ListItemTemplateMixin, ListView):
            pass  # No model defined

        view = BadListView()
        view.request = request_factory.get("/")
        view.object_list = []

        with pytest.raises(AttributeError) as exc_info:
            view.get_list_item_template()

        assert "missing a model" in str(exc_info.value)

    @pytest.mark.django_db
    def test_explicit_template_overrides_auto_generation(self, request_factory):
        """Test that explicit template takes precedence over auto-generation."""

        class ProductListView(ListItemTemplateMixin, ListView):
            model = Product
            list_item_template = "override/template.html"

        view = ProductListView()
        view.request = request_factory.get("/")
        view.object_list = Product.objects.none()

        context = view.get_context_data()

        assert context["list_item_template"] == "override/template.html"
        # Should not be the auto-generated name
        assert context["list_item_template"] != "example/list_product_item.html"

    @pytest.mark.django_db
    def test_mixin_works_with_multiple_inheritance(self, request_factory):
        """Test that mixin works correctly with multiple inheritance."""
        from mvp.views import SearchOrderMixin

        class ProductListView(ListItemTemplateMixin, SearchOrderMixin, ListView):
            model = Product
            search_fields = ["name", "description"]
            order_by = [("name", "Name"), ("-created_at", "Newest")]

        view = ProductListView()
        view.request = request_factory.get("/?q=test&o=name")
        view.object_list = Product.objects.none()

        context = view.get_context_data()

        # Check that all mixins contribute to context
        assert "list_item_template" in context
        assert "search_query" in context
        assert "order_by_choices" in context
        assert context["list_item_template"] == "example/list_product_item.html"

    @pytest.mark.django_db
    def test_template_name_with_article_model(self, request_factory):
        """Test template name generation for Article model."""

        class ArticleListView(ListItemTemplateMixin, ListView):
            model = Article

        view = ArticleListView()
        view.request = request_factory.get("/")
        view.object_list = Article.objects.none()

        template_name = view.get_list_item_template()

        assert template_name == "example/list_article_item.html"
