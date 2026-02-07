"""Integration tests for form_view.html template rendering."""

import pytest

from mvp.views import MVPFormView


class SimpleFormView(MVPFormView):
    """Test view for integration testing - doesn't use ContactForm to avoid sidebar rendering."""

    template_name = "mvp/form_view.html"
    page_title = "Test Form"
    success_url = "/success/"

    def get_form_class(self):
        """Return a simple form class."""
        from django import forms

        class TestForm(forms.Form):
            name = forms.CharField(max_length=100)
            email = forms.EmailField()
            message = forms.CharField(widget=forms.Textarea)

        return TestForm


@pytest.mark.django_db
class TestFormViewTemplateRendering:
    """Test suite for form_view.html template integration."""

    def test_template_renders_with_django_renderer(self, client):
        """T036: Template renders correctly with django renderer."""
        # Use the example app's contact form route
        response = client.get("/contact/")
        assert response.status_code == 200

        html = response.content.decode()

        # Verify structure
        assert "Contact Form (Auto Renderer)" in html
        assert '<form method="post">' in html
        assert 'name="name"' in html
        assert 'name="email"' in html
        assert 'name="message"' in html
        assert 'type="submit"' in html
        assert "Submit" in html

    def test_template_renders_with_crispy_renderer(self, client):
        """T037: Template renders correctly with crispy renderer when available."""
        pytest.importorskip("crispy_forms")

        response = client.get("/contact/")
        assert response.status_code == 200

        html = response.content.decode()

        # Verify crispy rendering
        assert "Contact Form (Auto Renderer)" in html
        assert '<form method="post">' in html
        # Crispy forms adds Bootstrap classes
        assert 'class="mb-3"' in html or 'class="form-group"' in html
        assert 'type="submit"' in html

    def test_template_renders_with_formset_renderer(self, client):
        """T038: Template renders correctly with formset renderer when available."""
        pytest.importorskip("formset")

        # This test is skipped because formset requires additional setup
        # The ContactForm view auto-detects and will use crispy or django
        pytest.skip("Formset renderer requires additional configuration")

    def test_template_displays_validation_errors(self, client):
        """T039: Template displays form validation errors correctly."""
        response = client.post(
            "/contact/",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "message": "Short",  # Too short - will fail validation
            },
        )

        assert response.status_code == 200  # Should re-render form with errors
        html = response.content.decode()

        # Verify error display
        assert "Message must be at least 10 characters" in html
        assert "Short" in html  # Should show the submitted value

    def test_template_card_structure(self, client):
        """Verify AdminLTE card structure is present."""
        response = client.get("/contact/")
        assert response.status_code == 200

        html = response.content.decode()

        # Verify card structure
        assert '<div class="card' in html
        assert "card-title" in html
        assert "card-body" in html
        assert "card-footer" in html

    def test_template_csrf_token_present(self, client):
        """Verify CSRF token is included in form."""
        response = client.get("/contact/")
        assert response.status_code == 200

        html = response.content.decode()

        # Verify CSRF token
        assert 'name="csrfmiddlewaretoken"' in html
        assert 'type="hidden"' in html


@pytest.mark.django_db
class TestMVPFormViewIntegration:
    """Test MVPFormView as a complete view."""

    def test_get_request_returns_200(self, client):
        """Test GET request returns form page."""
        response = client.get("/contact/")
        assert response.status_code == 200
        assert "Contact Form (Auto Renderer)" in response.content.decode()

    def test_post_valid_form_redirects(self, client):
        """Test POST with valid data redirects to success page."""
        response = client.post(
            "/contact/",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "message": "This is a test message with enough characters.",
            },
        )
        assert response.status_code == 302
        assert response.url == "/contact/success/"

    def test_post_invalid_form_shows_errors(self, client):
        """Test POST with invalid data shows errors."""
        response = client.post(
            "/contact/",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "message": "Short",  # Too short
            },
        )
        assert response.status_code == 200
        assert "Message must be at least 10 characters" in response.content.decode()


@pytest.mark.django_db
class TestExplicitRendererDemo:
    """Test suite for ExplicitRendererDemo view (T091)."""

    def test_explicit_renderer_demo_renders(self, client):
        """ExplicitRendererDemo should render with django renderer."""
        response = client.get("/explicit-renderer/")
        assert response.status_code == 200
        content = response.content.decode()

        # Verify page title
        assert "Explicit Renderer (Django)" in content

        # Verify form renderer is django (basic Django rendering)
        # Check for Django's default form rendering structure (no crispy classes)
        assert "form-control" not in content  # crispy adds this class
        assert "form-group" not in content  # crispy adds this class

    def test_explicit_renderer_uses_django_renderer(self, client):
        """ExplicitRendererDemo should use django renderer regardless of installed libs."""
        response = client.get("/explicit-renderer/")
        assert response.status_code == 200

        # Verify the view's form_renderer attribute is set to "django"
        from example.views import ExplicitRendererDemo

        view = ExplicitRendererDemo()
        assert hasattr(view, "form_renderer")
        assert view.form_renderer == "django"

    def test_explicit_renderer_form_submission(self, client):
        """ExplicitRendererDemo should handle form submission correctly."""
        response = client.post(
            "/explicit-renderer/",
            data={
                "name": "Test User",
                "email": "test@example.com",
                "message": "This is a test message with enough characters.",
            },
        )
        assert response.status_code == 302
        assert response["Location"] == "/contact/success/"
