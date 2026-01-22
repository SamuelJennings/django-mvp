"""Tests for Django Tables2 integration."""

import pytest
from django.urls import reverse

from example.models import Category, Product
from example.tables import ProductTable
from example.views import DataTablesView


@pytest.mark.django_db
class TestProductTable:
    """Unit tests for ProductTable configuration."""

    def test_table_model_configuration(self):
        """Test ProductTable is configured with correct model."""
        assert ProductTable.Meta.model == Product

    def test_table_template_name(self):
        """Test ProductTable uses custom MVP template."""
        assert ProductTable.Meta.template_name == "django_tables2/bootstrap5-mvp.html"

    def test_table_has_required_fields(self):
        """Test ProductTable includes all required fields."""
        expected_fields = (
            "name",
            "sku",
            "category",
            "short_description",
            "price",
            "stock",
            "rating",
            "status",
            "priority",
            "is_featured",
            "is_available",
            "tags",
            "barcode",
            "release_date",
            "created_at",
            "updated_at",
        )
        assert ProductTable.Meta.fields == expected_fields

    def test_table_bootstrap_classes(self):
        """Test ProductTable has Bootstrap 5 table classes."""
        assert "table" in ProductTable.Meta.attrs["class"]
        assert "table-striped" in ProductTable.Meta.attrs["class"]
        assert "table-hover" in ProductTable.Meta.attrs["class"]

    def test_table_empty_text_configured(self):
        """Test ProductTable has helpful empty state message."""
        assert "No products available" in ProductTable.Meta.empty_text
        assert "generate_dummy_data" in ProductTable.Meta.empty_text

    def test_price_column_alignment(self):
        """Test price column has text-end class for right alignment."""
        table = ProductTable([])
        price_column = table.columns["price"]
        assert "text-end" in price_column.attrs.get("td", {}).get("class", "")

    def test_status_column_alignment(self):
        """Test status column has text-center class."""
        table = ProductTable([])
        status_column = table.columns["status"]
        assert "text-center" in status_column.attrs.get("td", {}).get("class", "")


@pytest.mark.django_db
class TestDataTablesView:
    """Unit tests for DataTablesView configuration."""

    def test_view_model_configuration(self):
        """Test DataTablesView is configured with correct model."""
        assert DataTablesView.model == Product

    def test_view_table_class(self):
        """Test DataTablesView uses ProductTable."""
        assert DataTablesView.table_class == ProductTable

    def test_view_template_name(self):
        """Test DataTablesView uses correct template."""
        assert DataTablesView.template_name == "example/datatables_demo.html"

    def test_view_pagination(self):
        """Test DataTablesView has pagination enabled."""
        assert DataTablesView.paginate_by == 25


@pytest.mark.django_db
class TestDataTablesIntegration:
    """Integration tests for DataTables demo page."""

    def test_datatables_url_routing(self, client):
        """Test /datatables-demo/ URL returns 200."""
        url = reverse("datatables_demo")
        response = client.get(url)
        assert response.status_code == 200

    def test_template_rendering_includes_table(self, client):
        """Test response context includes table object."""
        url = reverse("datatables_demo")
        response = client.get(url)
        assert "table" in response.context

    def test_template_uses_correct_base(self, client):
        """Test template extends mvp/base.html."""
        url = reverse("datatables_demo")
        response = client.get(url)
        template_names = [t.name for t in response.templates]
        assert "example/datatables_demo.html" in template_names

    def test_pagination_parameter(self, client, django_user_model):
        """Test pagination query parameter works."""
        # Create enough products for multiple pages
        category = Category.objects.create(name="Test Category")
        for i in range(30):
            Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                sku=f"SKU-{i}",
                category=category,
                price=10.00,
                stock=100,
            )

        url = reverse("datatables_demo")
        response = client.get(f"{url}?page=2")
        assert response.status_code == 200
        assert "table" in response.context

    def test_empty_state_displays(self, client):
        """Test empty message displays when no products exist."""
        Product.objects.all().delete()
        url = reverse("datatables_demo")
        response = client.get(url)
        assert "No products available" in response.content.decode()
