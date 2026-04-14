"""
Smoke tests – quick sanity-checks that the package imports cleanly and
the Django configuration is valid.
"""

import django
import pytest


def test_django_version():
    """Django is available and meets the minimum version."""
    major, minor, *_ = django.VERSION
    assert (major, minor) >= (4, 2), f"Django {major}.{minor} < 4.2"


@pytest.mark.django_db
def test_mvp_apps_load(client):
    """Django can resolve the root URL without raising configuration errors."""
    response = client.get("/")
    assert response.status_code in {200, 301, 302, 404}


def test_mvp_imports():
    """The published package surface imports without errors."""
    import mvp  # noqa: F401
    from mvp import (
        renderers,  # noqa: F401
        views,  # noqa: F401
    )
    from mvp.templatetags import mvp as mvp_tags  # noqa: F401
