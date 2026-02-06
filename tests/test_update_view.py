"""
Tests for MVPUpdateView (User Story 3: Edit model instances with auto-detected form rendering).

This module tests MVPUpdateView which combines MVPFormViewMixin with Django's
UpdateView to provide model form edit views with AdminLTE card-based layouts
and automatic form renderer detection (crispy → formset → django).

Test Coverage:
- T066: Inheritance verification (MVPFormViewMixin + UpdateView)
- T067: Form rendering with pre-populated data
- T068: Model instance update on valid submission
- T069: Form redisplay with validation errors on invalid submission

Visual verification (T061-T065) completed manually with chrome-devtools-mcp:
- Form renders correctly with edit URL (/products/33/edit/)
- Form fields pre-populate with existing product data
- Update workflow completes successfully (price $99.99 → $149.99)
- Database update confirmed via Django shell
- Validation errors display correctly when name field is empty
"""

import pytest
from django.test import Client
from django.urls import path

from example.models import Category, Product
from mvp.views import MVPUpdateView


class ProductUpdateView(MVPUpdateView):
    """Test view for MVPUpdateView verification."""

    model = Product
    fields = ["name", "price", "description"]
    success_url = "/products/"
    page_title = "Edit Product"


# Add test URL pattern
urlpatterns = [
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="test_product_edit"),
]


@pytest.fixture
def test_product(db):
    """Create a test product for editing."""
    # Create a category first (ForeignKey requirement)
    category = Category.objects.create(name="Electronics", slug="electronics")

    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        description="Original description",
        price="99.99",
        stock=10,
        status="Draft",
    )


@pytest.mark.django_db
class TestMVPUpdateViewInheritance:
    """Test T066: MVPUpdateView inherits from MVPFormViewMixin and UpdateView."""

    def test_inherits_from_mvp_form_view_mixin(self):
        """MVPUpdateView should inherit from MVPFormViewMixin."""
        from mvp.views import MVPFormViewMixin

        assert issubclass(MVPUpdateView, MVPFormViewMixin)

    def test_inherits_from_django_update_view(self):
        """MVPUpdateView should inherit from Django's UpdateView."""
        from django.views.generic import UpdateView

        assert issubclass(MVPUpdateView, UpdateView)

    def test_has_form_view_mixin_attributes(self):
        """MVPUpdateView should have attributes from MVPFormViewMixin."""
        view = ProductUpdateView()
        assert hasattr(view, "get_form_renderer")
        assert hasattr(view, "get_context_data")

    def test_has_update_view_functionality(self):
        """MVPUpdateView should have UpdateView model binding attributes."""
        view = ProductUpdateView()
        assert hasattr(view, "model")
        assert hasattr(view, "fields")
        assert hasattr(view, "get_object")


@pytest.mark.django_db
class TestMVPUpdateViewFormRendering:
    """Test T067: MVPUpdateView renders edit form with pre-populated data."""

    def test_renders_edit_form_with_prepopulated_data(self, test_product, settings):
        """Edit form should display with existing product data pre-populated."""
        # Configure test URL
        settings.ROOT_URLCONF = __name__

        client = Client()
        response = client.get(f"/products/{test_product.pk}/edit/")

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Verify form fields are pre-populated with existing data
        assert f'value="{test_product.name}"' in content
        assert str(test_product.price) in content
        assert test_product.description in content

    def test_uses_mvp_template_with_card_layout(self, test_product, settings):
        """Edit form should use MVP template with card-based layout."""
        settings.ROOT_URLCONF = __name__

        client = Client()
        response = client.get(f"/products/{test_product.pk}/edit/")

        assert response.status_code == 200
        # Verify card structure
        assert b"card" in response.content
        assert b"Edit Product" in response.content  # page_title in card header

    def test_includes_csrf_token(self, test_product, settings):
        """Edit form should include CSRF token for security."""
        settings.ROOT_URLCONF = __name__

        client = Client()
        response = client.get(f"/products/{test_product.pk}/edit/")

        assert response.status_code == 200
        assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
class TestMVPUpdateViewModelUpdate:
    """Test T068: MVPUpdateView updates model instance on valid form submission."""

    def test_updates_product_on_valid_submission(self, test_product, settings):
        """Valid form submission should update existing product in database."""
        settings.ROOT_URLCONF = __name__

        client = Client()
        updated_data = {
            "name": "Updated Product Name",
            "price": "149.99",
            "description": "Updated description text",
        }
        response = client.post(f"/products/{test_product.pk}/edit/", updated_data)

        # Verify redirect to success_url
        assert response.status_code == 302
        assert response["Location"] == "/products/"

        # Verify database was updated
        test_product.refresh_from_db()
        assert test_product.name == "Updated Product Name"
        assert str(test_product.price) == "149.99"
        assert test_product.description == "Updated description text"

    def test_preserves_unchanged_fields(self, test_product, settings):
        """Fields not in form should remain unchanged after update."""
        settings.ROOT_URLCONF = __name__

        original_slug = test_product.slug
        original_stock = test_product.stock

        client = Client()
        updated_data = {
            "name": "Updated Name",
            "price": "149.99",
            "description": "Updated description",
        }
        client.post(f"/products/{test_product.pk}/edit/", updated_data)

        # Verify excluded fields remain unchanged
        test_product.refresh_from_db()
        assert test_product.slug == original_slug  # slug not in fields
        assert test_product.stock == original_stock  # stock not in fields


@pytest.mark.django_db
class TestMVPUpdateViewValidationErrors:
    """Test T069: MVPUpdateView redisplays form with errors on invalid submission."""

    def test_redisplays_form_with_errors_on_invalid_data(self, test_product, settings):
        """Invalid form submission should redisplay form with error messages."""
        settings.ROOT_URLCONF = __name__

        client = Client()
        # Submit with missing required field
        invalid_data = {
            "name": "",  # Empty required field
            "price": "149.99",
            "description": "Test description",
        }
        response = client.post(f"/products/{test_product.pk}/edit/", invalid_data)

        # Verify form redisplayed (no redirect)
        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Verify error message appears
        assert "This field is required" in content or "required" in content.lower()

    def test_preserves_valid_field_values_on_error(self, test_product, settings):
        """Valid field values should be preserved when form has errors."""
        settings.ROOT_URLCONF = __name__

        client = Client()
        invalid_data = {
            "name": "",  # Invalid
            "price": "149.99",  # Valid
            "description": "Test description",  # Valid
        }
        response = client.post(f"/products/{test_product.pk}/edit/", invalid_data)

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Verify valid values are preserved in form
        assert "149.99" in content
        assert "Test description" in content

    def test_does_not_update_database_on_validation_error(self, test_product, settings):
        """Database should not be modified when validation fails."""
        settings.ROOT_URLCONF = __name__

        original_name = test_product.name
        original_price = str(test_product.price)  # Convert Decimal to string for comparison

        client = Client()
        invalid_data = {
            "name": "",  # Invalid
            "price": "149.99",
            "description": "Test description",
        }
        client.post(f"/products/{test_product.pk}/edit/", invalid_data)

        # Verify database unchanged
        test_product.refresh_from_db()
        assert test_product.name == original_name
        assert str(test_product.price) == original_price
