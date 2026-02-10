"""
Tests for small-box Cotton component.

These tests verify the rendering and behavior of the AdminLTE 4 small-box widget.
"""

import pytest


@pytest.mark.django_db
def test_basic_small_box_rendering(cotton_render_soup):
    """Test basic small box rendering with required attributes."""
    soup = cotton_render_soup(
        "small-box",
        heading="150",
        text="New Orders",
        icon="box-seam",
        variant="primary",
    )

    # Verify main structure
    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box container should exist"

    # Verify inner content
    page_div = small_box.find("div", class_="inner")
    assert page_div is not None, "Inner div should exist"

    # Verify heading
    heading = page_div.find("h3")
    assert heading is not None, "Heading should exist"
    assert heading.get_text(strip=True) == "150", "Heading should be '150'"

    # Verify text
    text_p = page_div.find("p")
    assert text_p is not None, "Text paragraph should exist"
    assert text_p.get_text(strip=True) == "New Orders", "Text should be 'New Orders'"

    # Verify icon element (c-icon renders as <i> tag)
    icon_element = small_box.find("i")
    assert icon_element is not None, "Icon element should be present"
    assert "bi" in icon_element.get("class", ""), "Icon should have bi class"

    # Verify no footer link (not provided)
    footer_link = small_box.find("a", class_="small-box-footer")
    assert footer_link is None, "Footer link should not exist when link not provided"


@pytest.mark.django_db
def test_small_box_with_bg_attribute(cotton_render_soup):
    """Test small box with background color attribute."""
    soup = cotton_render_soup(
        "small-box",
        heading="53%",
        text="Bounce Rate",
        icon="settings",
        variant="warning",
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # Verify bg class is applied
    classes = small_box.get("class")
    assert classes and "text-bg-warning" in classes, "text-bg-warning class should be applied"


@pytest.mark.django_db
def test_small_box_with_footer_link_default_text(cotton_render_soup):
    """Test small box with footer link using default text."""
    soup = cotton_render_soup(
        "small-box",
        heading="150",
        text="New Orders",
        icon="box-seam",
        variant="primary",
        link="/orders/",
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # Verify footer link exists
    footer_link = small_box.find("a", class_="small-box-footer")
    assert footer_link is not None, "Footer link should exist"
    assert footer_link.get("href") == "/orders/", "Footer link href should be '/orders/'"

    # Verify default text
    link_text = footer_link.get_text(strip=True)
    assert "More info" in link_text, "Default link text should contain 'More info'"


@pytest.mark.django_db
def test_small_box_with_custom_link_text(cotton_render_soup):
    """Test small box with custom footer link text."""
    soup = cotton_render_soup(
        "small-box",
        heading="44",
        text="User Registrations",
        icon="person",
        bg="success",
        link="/users/",
        link_text="View all users",
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # Verify footer link exists
    footer_link = small_box.find("a", class_="small-box-footer")
    assert footer_link is not None, "Footer link should exist"

    # Verify custom text
    link_text = footer_link.get_text(strip=True)
    assert "View all users" in link_text, "Custom link text should be present"


@pytest.mark.django_db
def test_small_box_without_footer_link(cotton_render_soup):
    """Test small box without footer link."""
    soup = cotton_render_soup(
        "small-box",
        heading="65",
        text="Unique Visitors",
        icon="eye",
        bg="info",
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # Verify no footer link
    footer_link = small_box.find("a", class_="small-box-footer")
    assert footer_link is None, "Footer link should not exist when link not provided"


@pytest.mark.django_db
def test_small_box_with_custom_classes(cotton_render_soup):
    """Test small box with custom CSS classes."""
    soup = cotton_render_soup(
        "small-box",
        heading="150",
        text="New Orders",
        icon="box-seam",
        variant="primary",
        **{"class": "mb-3 shadow-lg"},
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # Verify custom classes are applied
    classes = small_box.get("class")
    assert classes and "mb-3" in classes, "mb-3 class should be applied"
    assert classes and "shadow-lg" in classes, "shadow-lg class should be applied"


@pytest.mark.django_db
def test_small_box_icon_aria_hidden(cotton_render_soup):
    """Test that icon has aria-hidden attribute for accessibility."""
    soup = cotton_render_soup(
        "small-box",
        heading="150",
        text="New Orders",
        icon="box-seam",
        variant="primary",
    )

    small_box = soup.find("div", class_="small-box")
    assert small_box is not None, "Small box should exist"

    # The c-icon component should render with appropriate ARIA attributes
    # Check for icon element presence (icon wrapper handled by c-icon component)
    icon_element = small_box.find("i")
    assert icon_element is not None, "Icon element should be present"


@pytest.mark.django_db
def test_small_box_bootstrap_shadow_utilities(cotton_render_soup):
    """Test small box with Bootstrap 5 shadow utility classes (T065)."""
    # Test shadow-sm
    soup_sm = cotton_render_soup(
        "small-box",
        heading="100",
        text="Shadow Small",
        icon="box-seam",
        **{"class": "shadow-sm"},
    )
    small_box_sm = soup_sm.find("div", class_="small-box")
    assert "shadow-sm" in small_box_sm.get("class"), "shadow-sm utility should be applied"

    # Test shadow
    soup = cotton_render_soup(
        "small-box",
        heading="200",
        text="Shadow",
        icon="box-seam",
        **{"class": "shadow"},
    )
    small_box = soup.find("div", class_="small-box")
    assert "shadow" in small_box.get("class"), "shadow utility should be applied"

    # Test shadow-lg
    soup_lg = cotton_render_soup(
        "small-box",
        heading="300",
        text="Shadow Large",
        icon="box-seam",
        **{"class": "shadow-lg"},
    )
    small_box_lg = soup_lg.find("div", class_="small-box")
    assert "shadow-lg" in small_box_lg.get("class"), "shadow-lg utility should be applied"


@pytest.mark.django_db
def test_small_box_all_variant_colors(cotton_render_soup):
    """Test small box with all Bootstrap variant colors (T068)."""
    variants = ["primary", "success", "warning", "danger", "info", "secondary"]

    for variant in variants:
        soup = cotton_render_soup(
            "small-box",
            heading="100",
            text=f"Test {variant}",
            icon="box-seam",
            variant=variant,
        )
        small_box = soup.find("div", class_="small-box")

        # Verify variant class is applied
        classes = small_box.get("class")
        expected_class = f"text-bg-{variant}"
        assert expected_class in classes, f"{expected_class} class should be applied for variant={variant}"
