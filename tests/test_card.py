"""Tests for the card component (v2.1)."""

import pytest
from bs4 import BeautifulSoup
from django_cotton import render_component


@pytest.fixture
def mock_request(rf):
    """Fixture providing a mock HTTP request using pytest-django's rf fixture."""
    return rf.get("/")


@pytest.mark.django_db
def test_basic_card_rendering(mock_request):
    """Test basic card rendering with title (body content rendering via _children has known Cotton limitation)."""
    html = render_component(
        mock_request,
        "card",
        title="Sample Card"
    )
    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="card")
    assert card is not None, "Card container should exist"

    header = card.find("div", class_="card-header")
    assert header is not None, "Card header should always exist in v2.1"
    assert "Sample Card" in header.text, "Card title should be in header"

    body = card.find("div", class_="card-body")
    assert body is not None, "Card body should exist"


@pytest.mark.django_db
def test_card_with_icon_in_header(mock_request):
    """Test card with icon in header (v2.1 flexbox layout)."""
    html = render_component(
        mock_request,
        "card",
        title="Settings",
        icon="briefcase"  # Use available Bootstrap icon
    )
    soup = BeautifulSoup(html, "html.parser")

    header = soup.find("div", class_="card-header")
    assert header is not None, "Card header should exist"
    assert "Settings" in header.text, "Title should be in header"
    
    # Check flexbox wrapper exists
    icon_wrapper = header.find("div", class_="d-inline-flex")
    assert icon_wrapper is not None, "Icon wrapper with flexbox should exist"


@pytest.mark.django_db
def test_card_with_variant_outline_fill(mock_request):
    """Test card with variant=primary and fill=outline (v2.1)."""
    html = render_component(
        mock_request,
        "card",
        title="Outline Card",
        variant="primary",
        fill="outline",
        _children="<p>Outline card content</p>"
    )
    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="card")
    assert card is not None, "Card container should exist"
    
    classes = card.get("class")
    assert "card-primary" in classes, "Card should have card-primary class"
    assert "card-outline" in classes, "Card should have card-outline class"


@pytest.mark.django_db
def test_card_with_compact_body(mock_request):
    """Test card with compact attribute for zero-padding body (v2.1 feature)."""
    html = render_component(
        mock_request,
        "card",
        title="Data Table",
        compact=True,
        _children='<table class="table mb-0"><tr><td>Data</td></tr></table>'
    )
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find("div", class_="card-body")
    assert body is not None, "Card body should exist"
    
    classes = body.get("class")
    assert "p-0" in classes, "Body should have p-0 class for compact mode"


@pytest.mark.django_db
def test_card_with_variant_card_fill(mock_request):
    """Test card with variant=warning and fill=card (v2.1)."""
    html = render_component(
        mock_request,
        "card",
        title="Full Card Fill",
        variant="warning",
        fill="card",
        _children="<p>Full card fill content</p>"
    )
    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="card")
    assert card is not None, "Card container should exist"
    
    classes = card.get("class")
    assert "text-bg-warning" in classes, "Card should have text-bg-warning class"


@pytest.mark.django_db
def test_card_without_title_always_has_header(mock_request):
    """Test that card header always renders in v2.1 even without title."""
    html = render_component(
        mock_request,
        "card",
        _children="<p>Just body content</p>"
    )
    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="card")
    assert card is not None, "Card container should exist"
    
    # Header ALWAYS exists in v2.1
    header = card.find("div", class_="card-header")
    assert header is not None, "Card header should always exist in v2.1"


@pytest.mark.django_db
def test_card_with_custom_classes(mock_request):
    """Test card with custom class passthrough (v2.1 uses 'class' attribute)."""
    html = render_component(
        mock_request,
        "card",
        title="Custom Card",
        **{"class": "mb-3 shadow-lg"},
        _children="<p>Custom card content</p>"
    )
    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="card")
    assert card is not None, "Card container should exist"
    
    classes = card.get("class")
    assert "mb-3" in classes, "Card should have mb-3 class"
    assert "shadow-lg" in classes, "Card should have shadow-lg class"


@pytest.mark.django_db
def test_card_all_variant_fill_combinations(mock_request):
    """Test card with all variant-fill combinations (v2.1: outline and card only)."""
    variants = ["primary", "success", "warning", "danger", "info", "secondary"]
    fills = ["outline", "card"]  # v2.0 removed "header" option
    
    for variant in variants:
        for fill in fills:
            html = render_component(
                mock_request,
                "card",
                title=f"Test {variant}-{fill}",
                variant=variant,
                fill=fill,
                _children="<p>Content</p>"
            )
            soup = BeautifulSoup(html, "html.parser")
            card = soup.find("div", class_="card")
            assert card is not None, f"Card should exist for {variant}-{fill}"
            
            classes = card.get("class")
            if fill == "outline":
                assert f"card-{variant}" in classes, f"Should have card-{variant} for outline"
                assert "card-outline" in classes, "Should have card-outline"
            elif fill == "card":
                assert f"text-bg-{variant}" in classes, f"Should have text-bg-{variant} for card fill"
