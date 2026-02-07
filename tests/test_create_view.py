"""Tests for MVPCreateView functionality."""

import pytest

from example.models import Category, Product
from mvp.views import MVPCreateView


@pytest.mark.django_db
class TestMVPCreateView:
    """Test suite for MVPCreateView class."""

    def test_mvpcreateview_inherits_from_mixin_and_createview(self):
        """T051: MVPCreateView should inherit from MVPFormViewMixin and CreateView."""
        from django.views.generic.edit import CreateView

        from mvp.views import MVPFormViewMixin

        # Check that MVPCreateView is a subclass of both
        assert issubclass(MVPCreateView, MVPFormViewMixin)
        assert issubclass(MVPCreateView, CreateView)

    def test_mvpcreateview_renders_create_form(self, client):
        """T052: MVPCreateView should render model create form correctly."""
        response = client.get("/products/create/")

        assert response.status_code == 200

        html = response.content.decode()

        # Verify page title
        assert "Create Product (Model Form)" in html

        # Verify form fields are present
        assert 'name="name"' in html
        assert 'name="slug"' in html
        assert 'name="category"' in html
        assert 'name="description"' in html
        assert 'name="price"' in html
        assert 'name="stock"' in html
        assert 'name="status"' in html

        # Verify submit button
        assert 'type="submit"' in html
        assert "Submit" in html

    def test_mvpcreateview_saves_instance_on_valid_submission(self, client):
        """T053: MVPCreateView should save model instance on valid submission."""
        # Create a test category first
        category = Category.objects.create(name="Test Category", slug="test-category")

        # Get initial count
        initial_count = Product.objects.count()

        # Submit valid form data
        response = client.post(
            "/products/create/",
            data={
                "name": "Integration Test Product",
                "slug": "integration-test-product",
                "category": category.id,
                "description": "Test product description",
                "price": "49.99",
                "stock": "5",
                "status": "draft",
            },
        )

        # Should redirect to success_url
        assert response.status_code == 302
        assert response.url == "/products/"

        # Verify product was created
        assert Product.objects.count() == initial_count + 1

        # Verify product data
        product = Product.objects.get(slug="integration-test-product")
        assert product.name == "Integration Test Product"
        assert str(product.price) == "49.99"
        assert product.stock == 5
        assert product.status == "draft"
        assert product.category == category

    def test_mvpcreateview_redisplays_form_with_errors_on_invalid_submission(self, client):
        """T054: MVPCreateView should redisplay form with errors on invalid submission."""
        # Submit form with missing required fields
        response = client.post(
            "/products/create/",
            data={
                "name": "",  # Required field left empty
                "slug": "",  # Required field left empty
                # Missing category, description, price, stock
            },
        )

        # Should return 200 (form redisplay, not redirect)
        assert response.status_code == 200

        html = response.content.decode()

        # Verify error messages are displayed
        assert "This field is required" in html

        # Verify form is still present
        assert '<form method="post">' in html
        assert 'name="name"' in html
        assert 'name="slug"' in html
