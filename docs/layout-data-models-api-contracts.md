# AdminLTE Layout Configuration: Data Models & API Contracts

## Data Models

### 1. Layout Configuration Data Model

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union
from enum import Enum

class BreakpointType(Enum):
    """Bootstrap responsive breakpoints for sidebar expansion."""
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    XXL = "xxl"

@dataclass(frozen=True)
class LayoutConfig:
    """
    Immutable configuration for AdminLTE layout options.

    This dataclass represents the complete layout state including:
    - Fixed positioning for major layout components
    - Responsive sidebar behavior
    - Generated CSS classes for body element
    """

    # Core layout attributes
    fixed_sidebar: bool = False
    fixed_header: bool = False
    fixed_footer: bool = False
    sidebar_expand: BreakpointType = BreakpointType.LG

    # Derived properties (computed from above attributes)
    @property
    def body_classes(self) -> str:
        """Generate AdminLTE body classes from configuration."""
        classes = ["bg-body-tertiary"]  # Base AdminLTE theme class

        # Add responsive sidebar class (always present)
        classes.append(f"sidebar-expand-{self.sidebar_expand.value}")

        # Add fixed positioning classes when enabled
        if self.fixed_sidebar:
            classes.append("layout-fixed")
        if self.fixed_header:
            classes.append("layout-navbar-fixed")
        if self.fixed_footer:
            classes.append("layout-footer-fixed")

        return " ".join(classes)

    # Validation methods
    def validate(self) -> List[str]:
        """
        Validate configuration and return list of errors.

        Returns:
            List[str]: Empty list if valid, error messages if invalid
        """
        errors = []

        # Validate breakpoint enum value
        if not isinstance(self.sidebar_expand, BreakpointType):
            errors.append(f"Invalid sidebar_expand: {self.sidebar_expand}")

        # Business rule validations (if any)
        # Currently no conflicting combinations, but could be added

        return errors

    @classmethod
    def from_request_params(cls, params: Dict[str, str]) -> 'LayoutConfig':
        """
        Create LayoutConfig from HTTP query parameters.

        Args:
            params: Dictionary of query parameters from request.GET

        Returns:
            LayoutConfig: Validated configuration instance
        """
        # Parse boolean checkbox parameters ('on' when checked, absent when unchecked)
        fixed_sidebar = params.get('fixed_sidebar') == 'on'
        fixed_header = params.get('fixed_header') == 'on'
        fixed_footer = params.get('fixed_footer') == 'on'

        # Parse breakpoint with fallback to default
        breakpoint_str = params.get('breakpoint', 'lg')
        try:
            sidebar_expand = BreakpointType(breakpoint_str)
        except ValueError:
            sidebar_expand = BreakpointType.LG  # Fallback to default

        return cls(
            fixed_sidebar=fixed_sidebar,
            fixed_header=fixed_header,
            fixed_footer=fixed_footer,
            sidebar_expand=sidebar_expand
        )

    @classmethod
    def from_component_attrs(cls, attrs: Dict[str, Any]) -> 'LayoutConfig':
        """
        Create LayoutConfig from Cotton component attributes.

        Args:
            attrs: Dictionary of component attributes

        Returns:
            LayoutConfig: Configuration instance
        """
        # Handle both boolean and string representations
        def parse_bool(value: Any) -> bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)

        return cls(
            fixed_sidebar=parse_bool(attrs.get('fixed_sidebar', False)),
            fixed_header=parse_bool(attrs.get('fixed_header', False)),
            fixed_footer=parse_bool(attrs.get('fixed_footer', False)),
            sidebar_expand=BreakpointType(attrs.get('sidebar_expand', 'lg'))
        )

@dataclass
class LayoutState:
    """
    Mutable layout state stored in request object.

    Used by template tags to communicate layout configuration
    to the context processor during template rendering.
    """

    config: Optional[LayoutConfig] = None
    source: str = "default"  # Track configuration source for debugging

    def set_config(self, config: LayoutConfig, source: str = "unknown") -> None:
        """Update layout configuration."""
        self.config = config
        self.source = source

    def get_body_classes(self) -> str:
        """Get body classes, falling back to defaults if no config set."""
        if self.config:
            return self.config.body_classes
        # Default AdminLTE classes
        return "bg-body-tertiary sidebar-expand-lg"

### 2. Settings Configuration Schema

@dataclass
class MVPLayoutDefaults:
    """Default layout configuration from Django settings."""

    fixed_sidebar: bool = False
    fixed_header: bool = False
    fixed_footer: bool = False
    sidebar_expand: str = "lg"
    body_class: str = "bg-body-tertiary sidebar-expand-lg"

    @classmethod
    def from_settings(cls, settings_dict: Dict[str, Any]) -> 'MVPLayoutDefaults':
        """Create from MVP.layout settings dictionary."""
        layout_settings = settings_dict.get('layout', {})

        return cls(
            fixed_sidebar=layout_settings.get('fixed_sidebar', False),
            fixed_header=layout_settings.get('fixed_header', False),
            fixed_footer=layout_settings.get('fixed_footer', False),
            sidebar_expand=layout_settings.get('sidebar_expand', 'lg'),
            body_class=layout_settings.get('body_class', 'bg-body-tertiary sidebar-expand-lg')
        )
```

## API Contracts

### 1. HTTP Endpoint Contract - Demo Page

```yaml
# OpenAPI 3.0 specification for layout demo endpoint
openapi: 3.0.0
info:
  title: AdminLTE Layout Demo API
  version: 1.0.0
  description: Interactive layout configuration demo endpoint

paths:
  /layout/:
    get:
      summary: AdminLTE Layout Configuration Demo
      description: |
        Interactive demo page for testing AdminLTE layout configurations.
        Accepts layout parameters via query string and renders a demonstration
        page with configuration form controls.
      parameters:
        - name: fixed_sidebar
          in: query
          required: false
          description: Enable fixed sidebar positioning
          schema:
            type: string
            enum: ["on"]
          example: "on"

        - name: fixed_header
          in: query
          required: false
          description: Enable fixed header positioning
          schema:
            type: string
            enum: ["on"]
          example: "on"

        - name: fixed_footer
          in: query
          required: false
          description: Enable fixed footer positioning
          schema:
            type: string
            enum: ["on"]
          example: "on"

        - name: breakpoint
          in: query
          required: false
          description: Bootstrap breakpoint for sidebar expansion
          schema:
            type: string
            enum: ["sm", "md", "lg", "xl", "xxl"]
            default: "lg"
          example: "lg"

      responses:
        200:
          description: Rendered HTML demo page
          content:
            text/html:
              schema:
                type: string
              examples:
                default_layout:
                  summary: Default layout (no fixed elements)
                  value: "<html><!-- Demo page with default layout --></html>"
                fixed_sidebar:
                  summary: Fixed sidebar layout
                  value: "<html><!-- Demo page with fixed sidebar --></html>"

        400:
          description: Invalid query parameters
          content:
            text/html:
              schema:
                type: string
              example: "<html><!-- Error page --></html>"

# Example requests:
# GET /layout/
# GET /layout/?fixed_sidebar=on&breakpoint=lg
# GET /layout/?fixed_sidebar=on&fixed_header=on&fixed_footer=on&breakpoint=xl
```

### 2. Context Processor Interface Contract

```python
from typing import Dict, Any
from django.http import HttpRequest

def mvp_config(request: HttpRequest) -> Dict[str, Any]:
    """
    Enhanced context processor providing MVP configuration to templates.

    Contract:
    - MUST provide 'mvp' key in returned dictionary
    - MUST include layout configuration with body_classes
    - MUST merge settings defaults with request-level overrides
    - MUST handle missing/invalid configurations gracefully

    Args:
        request: Django HttpRequest object (may contain layout state)

    Returns:
        Dict containing:
        - mvp.layout.body_class: Complete CSS class string for <body> element
        - mvp.layout.config: Current LayoutConfig instance (if any)
        - mvp.brand: Site branding configuration
        - mvp.sidebar: Sidebar configuration
        - mvp.footer: Footer configuration
        - mvp.actions: Navbar action widgets

    Template Usage:
        <body class="{{ mvp.layout.body_class }}">

    Request State Contract:
        - Layout state stored at request._mvp_layout_state (optional)
        - If present, overrides settings defaults
        - If absent, uses MVP settings defaults
    """
    pass  # Implementation details in actual code

# Context processor registration in settings.py:
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'mvp.context_processors.mvp_config',  # Must be included
            ],
        },
    },
]
```

### 3. Template Tag Interface Contract

```python
from django import template
from django.http import HttpRequest
from typing import Any, Dict

register = template.Library()

@register.simple_tag(takes_context=True)
def set_layout_config(context: Dict[str, Any], **kwargs) -> str:
    """
    Template tag to configure AdminLTE layout from component attributes.

    Contract:
    - MUST accept layout attribute keywords (fixed_sidebar, fixed_header, etc.)
    - MUST store configuration in request._mvp_layout_state for context processor
    - MUST validate attribute values and provide sensible defaults
    - MUST return empty string (side-effect only tag)

    Args:
        context: Django template context (must contain 'request')
        **kwargs: Layout configuration attributes

    Supported Kwargs:
        fixed_sidebar (bool): Enable fixed sidebar positioning
        fixed_header (bool): Enable fixed header positioning
        fixed_footer (bool): Enable fixed footer positioning
        sidebar_expand (str): Bootstrap breakpoint (sm, md, lg, xl, xxl)

    Returns:
        str: Empty string (side-effect only)

    Template Usage:
        {% load layout_tags %}
        {% set_layout_config fixed_sidebar=True fixed_header=True sidebar_expand="lg" %}

    Cotton Component Usage:
        <!-- In cotton/adminlte/app.html -->
        <c-vars fixed_sidebar fixed_header fixed_footer sidebar_expand="lg" />
        {% load layout_tags %}
        {% set_layout_config fixed_sidebar=fixed_sidebar fixed_header=fixed_header
                             fixed_footer=fixed_footer sidebar_expand=sidebar_expand %}
        <div class="app-wrapper">{{ slot }}</div>

    Error Handling:
        - Invalid breakpoint values fall back to 'lg'
        - Missing request in context logs warning and no-ops
        - Non-boolean values for fixed_* attributes are coerced to boolean
    """
    pass  # Implementation details in actual code

# Template tag loading:
# {% load layout_tags %}
```

### 4. Django Settings Configuration Schema

```python
# settings.py configuration schema

MVP = {
    # Layout configuration (optional, provides defaults)
    "layout": {
        # Fixed positioning options (default: False for all)
        "fixed_sidebar": False,   # bool: Fix sidebar position
        "fixed_header": False,    # bool: Fix header position
        "fixed_footer": False,    # bool: Fix footer position

        # Responsive behavior (default: "lg")
        "sidebar_expand": "lg",   # str: Bootstrap breakpoint (sm|md|lg|xl|xxl)

        # Explicit body class override (optional)
        "body_class": "bg-body-tertiary sidebar-expand-lg",  # str: Complete CSS classes
    },

    # Other MVP configuration sections
    "brand": {
        "text": "My Application",
        "logo": "img/logo.png",
        "icon": "img/favicon.ico",
    },
    "sidebar": {
        "visible": True,
        "width": "280px",
    },
    "footer": {
        "visible": True,
        "text": "© 2026 My Application",
    },
    "actions": [
        {"icon": "github", "text": "GitHub", "href": "https://github.com/...", "target": "_blank"},
    ],
}

# Configuration validation:
# - All layout fields are optional with sensible defaults
# - Invalid sidebar_expand values fall back to "lg"
# - body_class can override automatic class generation
# - Configuration merged with hardcoded defaults in context processor
```

### 5. Cotton Component Interface Contract

```html
<!-- Cotton component: cotton/adminlte/app.html -->
<!--
Component Contract:
- Accepts layout attribute props (fixed_sidebar, fixed_header, fixed_footer, sidebar_expand)
- Converts attributes to layout configuration via template tag
- Renders app wrapper structure without layout classes (body handles those)
- Provides slot for child content

Props:
- fixed_sidebar (boolean): Enable fixed sidebar positioning
- fixed_header (boolean): Enable fixed header positioning
- fixed_footer (boolean): Enable fixed footer positioning
- sidebar_expand (string): Bootstrap breakpoint for sidebar expansion (sm|md|lg|xl|xxl)

Template Integration:
- Uses c-vars to accept attributes as template variables
- Calls set_layout_config template tag to store configuration
- Layout classes applied to <body> by base template, not this component

Usage Examples:
  {% cotton 'adminlte/app' %}
    <!-- Default layout -->
    <h1>My Content</h1>
  {% endcotton %}

  {% cotton 'adminlte/app' fixed_sidebar=True fixed_header=True sidebar_expand="xl" %}
    <!-- Fixed sidebar + header, XL breakpoint -->
    <h1>My Content</h1>
  {% endcotton %}
-->

<c-vars fixed_sidebar=False fixed_header=False fixed_footer=False sidebar_expand="lg" />

{% load layout_tags %}
{% set_layout_config
   fixed_sidebar=fixed_sidebar
   fixed_header=fixed_header
   fixed_footer=fixed_footer
   sidebar_expand=sidebar_expand %}

<div class="app-wrapper">
  {{ slot }}
</div>
```

## Data Flow Summary

```
1. Demo Page Request → Query Parameters → LayoutConfig.from_request_params()
2. Cotton Component → Attributes → LayoutConfig.from_component_attrs()
3. Template Tag → LayoutConfig → Request Storage (request._mvp_layout_state)
4. Context Processor → LayoutConfig → CSS Classes → Template Context
5. Base Template → Body Classes → HTML Rendering
```

## Validation & Error Handling

1. **Invalid Breakpoints**: Fall back to "lg" default
2. **Missing Request Context**: Template tag logs warning and no-ops
3. **Type Conversion**: Non-boolean values coerced to boolean
4. **Configuration Conflicts**: No current conflicts, extensible for future rules
5. **Missing Configuration**: Context processor provides sensible defaults

## Testing Contracts

```python
# Data model tests
def test_layout_config_generates_correct_body_classes():
    """Test body class generation from configuration."""

def test_layout_config_from_request_params():
    """Test parsing query parameters to configuration."""

def test_layout_config_validation():
    """Test configuration validation rules."""

# API endpoint tests
def test_demo_page_accepts_query_parameters():
    """Test demo page handles all query parameter combinations."""

def test_demo_page_renders_configuration_form():
    """Test demo page includes interactive form controls."""

# Template tag tests
def test_set_layout_config_stores_in_request():
    """Test template tag stores configuration in request state."""

def test_set_layout_config_handles_invalid_values():
    """Test template tag error handling and defaults."""

# Context processor tests
def test_mvp_config_provides_layout_classes():
    """Test context processor generates body classes."""

def test_mvp_config_merges_settings_with_request():
    """Test priority of request overrides vs settings defaults."""
```
