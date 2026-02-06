"""Unit tests for MVPFormViewMixin functionality."""

import logging
from unittest.mock import patch

import pytest
from django import forms
from django.http import HttpRequest
from django.views.generic import FormView

from mvp.views import MVPFormView, MVPFormViewMixin


class SimpleForm(forms.Form):
    """Test form for MVPFormViewMixin testing."""

    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class TestFormView(MVPFormViewMixin, FormView):
    """Test view combining MVPFormViewMixin with FormView."""

    form_class = SimpleForm
    template_name = "mvp/form_view.html"
    success_url = "/success/"
    page_title = "Test Form"


@pytest.mark.django_db
class TestMVPFormViewMixinRendererDetection:
    """Test suite for get_form_renderer() auto-detection logic."""

    def test_auto_detection_crispy_installed(self):
        """T029: Auto-detection prioritizes crispy_forms when installed."""
        view = TestFormView()
        with patch("mvp.utils.app_is_installed") as mock_app_check:
            # Simulate crispy_forms installed
            mock_app_check.side_effect = lambda app: app == "crispy_forms"

            renderer = view.get_form_renderer()

            assert renderer == "crispy"
            # Should check crispy_forms first
            mock_app_check.assert_any_call("crispy_forms")

    def test_auto_detection_formset_installed(self):
        """T029: Auto-detection falls back to formset when crispy not available."""
        view = TestFormView()
        with patch("mvp.utils.app_is_installed") as mock_app_check:
            # Simulate only formset installed
            mock_app_check.side_effect = lambda app: app == "formset"

            renderer = view.get_form_renderer()

            assert renderer == "formset"
            # Should check both crispy and formset
            mock_app_check.assert_any_call("crispy_forms")
            mock_app_check.assert_any_call("formset")

    def test_auto_detection_django_fallback(self):
        """T029: Auto-detection falls back to django when no renderers installed."""
        view = TestFormView()
        with patch("mvp.utils.app_is_installed") as mock_app_check:
            # Simulate no form renderers installed
            mock_app_check.return_value = False

            renderer = view.get_form_renderer()

            assert renderer == "django"


@pytest.mark.django_db
class TestMVPFormViewMixinExplicitRenderer:
    """Test suite for explicit renderer override behavior."""

    def test_explicit_renderer_crispy(self):
        """T030: Explicit renderer='crispy' is respected when available."""
        view = TestFormView()
        view.form_renderer = "crispy"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.side_effect = lambda app: app == "crispy_forms"

            renderer = view.get_form_renderer()

            assert renderer == "crispy"

    def test_explicit_renderer_formset(self):
        """T031: Explicit renderer='formset' is respected when available."""
        view = TestFormView()
        view.form_renderer = "formset"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.side_effect = lambda app: app == "formset"

            renderer = view.get_form_renderer()

            assert renderer == "formset"

    def test_explicit_renderer_django(self):
        """T032: Explicit renderer='django' is always respected (no dependency)."""
        view = TestFormView()
        view.form_renderer = "django"

        renderer = view.get_form_renderer()

        assert renderer == "django"


@pytest.mark.django_db
class TestMVPFormViewMixinInvalidRenderer:
    """Test suite for invalid renderer handling."""

    def test_invalid_renderer_crispy_not_installed(self, caplog):
        """T033: Fallback to django when crispy specified but not installed."""
        view = TestFormView()
        view.form_renderer = "crispy"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.return_value = False

            with caplog.at_level(logging.WARNING):
                renderer = view.get_form_renderer()

            assert renderer == "django"
            assert "crispy" in caplog.text
            assert "not installed" in caplog.text

    def test_invalid_renderer_formset_not_installed(self, caplog):
        """T033: Fallback to django when formset specified but not installed."""
        view = TestFormView()
        view.form_renderer = "formset"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.return_value = False

            with caplog.at_level(logging.WARNING):
                renderer = view.get_form_renderer()

            assert renderer == "django"
            assert "formset" in caplog.text
            assert "not installed" in caplog.text

    def test_warning_logged_for_unavailable_renderer(self, caplog):
        """T034: Warning is logged when explicit renderer is unavailable."""
        view = TestFormView()
        view.form_renderer = "crispy"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.return_value = False

            with caplog.at_level(logging.WARNING):
                view.get_form_renderer()

            # Check warning was logged
            assert len(caplog.records) > 0
            assert caplog.records[0].levelname == "WARNING"
            assert "MVPFormViewMixin" in caplog.records[0].message


@pytest.mark.django_db
class TestMVPFormViewMixinContextData:
    """Test suite for get_context_data() method."""

    def test_context_data_injects_renderer_and_title(self):
        """T035: get_context_data() injects form_renderer and page_title."""
        view = TestFormView()
        view.page_title = "Test Page Title"

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.return_value = False  # Use django renderer

            # Call get_context_data (need to setup request)
            request = HttpRequest()
            request.method = "GET"
            view.request = request
            view.kwargs = {}

            context = view.get_context_data()

            assert "form_renderer" in context
            assert context["form_renderer"] == "django"
            assert "page_title" in context
            assert context["page_title"] == "Test Page Title"

    def test_context_data_preserves_existing_context(self):
        """T035: get_context_data() preserves context from parent classes."""
        view = TestFormView()

        with patch("mvp.utils.app_is_installed") as mock_app_check:
            mock_app_check.return_value = False

            request = HttpRequest()
            request.method = "GET"
            view.request = request
            view.kwargs = {}

            context = view.get_context_data(custom_key="custom_value")

            # Should have both mixin context and custom context
            assert "form_renderer" in context
            assert "page_title" in context
            assert "custom_key" in context
            assert context["custom_key"] == "custom_value"


@pytest.mark.django_db
class TestMVPFormView:
    """Test suite for MVPFormView class."""

    def test_mvpformview_inherits_mixin_and_formview(self):
        """Verify MVPFormView combines MVPFormViewMixin and FormView."""
        assert issubclass(MVPFormView, MVPFormViewMixin)
        assert issubclass(MVPFormView, FormView)

    def test_mvpformview_default_template(self):
        """Verify MVPFormView uses correct default template."""
        assert MVPFormView.template_name == "mvp/form_view.html"
