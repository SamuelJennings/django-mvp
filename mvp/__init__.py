"""Django Cotton Layouts - Application layouts and UI patterns for Django Cotton."""

from mvp.utils import app_is_installed
from mvp.views import MVPCreateView, MVPFormView, MVPFormViewMixin, MVPUpdateView

__version__ = "0.1.0"

default_app_config = "mvp.apps.CottonLayoutsConfig"

__all__ = [
    "MVPCreateView",
    "MVPFormView",
    "MVPFormViewMixin",
    "MVPUpdateView",
    "app_is_installed",
]
