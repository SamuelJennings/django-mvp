"""
Tests for info-box Cotton component.

These tests verify the rendering and behavior of the AdminLTE 4 info-box widget.
"""

import pytest


@pytest.mark.django_db
def test_basic_info_box_rendering(cotton_render_soup):
    """Test basic info box rendering with required attributes."""
    soup = cotton_render_soup(
        "info-box",
        icon="settings",
        text="CPU Traffic",
        number="10%",
    )

    # Verify main structure
    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box container should exist"

    # Verify icon container
    icon_span = info_box.find("span", class_="info-box-icon")
    assert icon_span is not None, "Icon span should exist"
    assert icon_span.get("aria-hidden") == "true", "Icon should be aria-hidden"

    # Verify icon element (c-icon renders as <i> tag)
    icon_element = icon_span.find("i")
    assert icon_element is not None, "Icon element should be present"
    assert "bi" in icon_element.get("class", []), "Icon should have bi class"

    # Verify content
    content_div = info_box.find("div", class_="info-box-content")
    assert content_div is not None, "Content div should exist"

    text_span = content_div.find("span", class_="info-box-text")
    assert text_span is not None, "Text span should exist"
    assert text_span.get_text(strip=True) == "CPU Traffic", "Text should be 'CPU Traffic'"

    number_span = content_div.find("span", class_="info-box-number")
    assert number_span is not None, "Number span should exist"
    assert number_span.get_text(strip=True) == "10%", "Number should be '10%'"

    # Verify no progress bar (not provided)
    progress_div = content_div.find("div", class_="progress")
    assert progress_div is None, "Progress bar should not exist when not provided"


@pytest.mark.django_db
def test_info_box_with_variant_attribute(cotton_render_soup):
    """Test info box with variant color attribute (default fill='icon' mode)."""
    soup = cotton_render_soup(
        "info-box",
        icon="box-seam",
        text="Sales",
        number="13,648",
        variant="success",
    )

    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box should exist"

    # With fill="icon" (default), variant class should be on icon span
    icon_span = info_box.find("span", class_="info-box-icon")
    assert icon_span is not None, "Icon span should exist"

    icon_classes = icon_span.get("class")
    if icon_classes:
        assert (
            "text-bg-success" in icon_classes
        ), "text-bg-success class should be applied to icon span in default fill mode"


@pytest.mark.django_db
def test_info_box_with_progress_bar(cotton_render_soup):
    """Test info box with progress bar (now using c-progress component)."""
    soup = cotton_render_soup(
        "info-box",
        icon="add",
        text="Downloads",
        number="114,381",
        variant="info",
        progress="70",
        description="70% Increase in 30 Days",
    )

    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box should exist"

    content_div = info_box.find("div", class_="info-box-content")
    assert content_div is not None, "Content div should exist"

    # Verify progress bar exists (rendered by c-progress component)
    progress_div = content_div.find("div", class_="progress")
    assert progress_div is not None, "Progress bar should exist"

    # Verify ARIA attributes (tested in separate test, basic check here)
    assert progress_div.get("role") == "progressbar", "Progress should have progressbar role"
    assert progress_div.get("aria-valuenow") == "70", "Progress should have aria-valuenow=70"

    # Verify inner progress bar (c-progress uses calc() for width)
    progress_bar = progress_div.find("div", class_="progress-bar")
    assert progress_bar is not None, "Inner progress bar should exist"
    style = progress_bar.get("style")
    # c-progress component uses calc() formula for width
    assert style and "width:" in style and "70" in style, "Progress bar width should include 70"

    # Verify description
    description_span = content_div.find("span", class_="progress-description")
    assert description_span is not None, "Description span should exist"
    assert description_span.get_text(strip=True) == "70% Increase in 30 Days", "Description should match"


@pytest.mark.django_db
def test_info_box_with_box_fill_mode(cotton_render_soup):
    """Test info box with fill='box' mode (entire box colored)."""
    soup = cotton_render_soup(
        "info-box",
        icon="book",
        text="Bookmarks",
        number="41,410",
        variant="warning",
        fill="box",
    )

    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box should exist"

    # Verify text-bg-* class is applied to the entire box
    classes = info_box.get("class")
    assert classes and "text-bg-warning" in classes, "text-bg-warning class should be applied to box"

    # Verify icon span does NOT have text-bg-* class (only box is colored)
    icon_span = info_box.find("span", class_="info-box-icon")
    icon_classes = icon_span.get("class") if icon_span else None
    assert (
        icon_classes and "text-bg-warning" not in icon_classes
    ), "Icon span should not have text-bg class in box fill mode"


@pytest.mark.django_db
def test_info_box_with_custom_classes(cotton_render_soup):
    """Test info box with custom CSS classes."""
    soup = cotton_render_soup(
        "info-box",
        icon="settings",
        text="CPU Traffic",
        number="10%",
        **{"class": "mb-3 shadow-lg"},
    )

    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box should exist"

    # Verify custom classes are applied
    classes = info_box.get("class")
    assert classes and "mb-3" in classes, "mb-3 class should be applied"
    assert classes and "shadow-lg" in classes, "shadow-lg class should be applied"


@pytest.mark.django_db
def test_info_box_progress_bar_aria_attributes(cotton_render_soup):
    """Test ARIA attributes on progress bar for accessibility."""
    soup = cotton_render_soup(
        "info-box",
        icon="add",
        text="Downloads",
        number="114,381",
        progress="45",
    )

    info_box = soup.find("div", class_="info-box")
    assert info_box is not None, "Info box should exist"

    progress_div = info_box.find("div", class_="progress")
    assert progress_div is not None, "Progress bar should exist"

    # Verify all required ARIA attributes
    assert progress_div.get("role") == "progressbar", "Progress should have role='progressbar'"
    assert progress_div.get("aria-valuenow") == "45", "Progress should have aria-valuenow='45'"
    assert progress_div.get("aria-valuemin") == "0", "Progress should have aria-valuemin='0'"
    assert progress_div.get("aria-valuemax") == "100", "Progress should have aria-valuemax='100'"


@pytest.mark.django_db
def test_info_box_bootstrap_shadow_utilities(cotton_render_soup):
    """Test info box with Bootstrap 5 shadow utility classes (T064)."""
    # Test shadow-sm
    soup_sm = cotton_render_soup(
        "info-box",
        icon="box-seam",
        text="Shadow Small",
        number="100",
        **{"class": "shadow-sm"},
    )
    info_box_sm = soup_sm.find("div", class_="info-box")
    assert "shadow-sm" in info_box_sm.get("class"), "shadow-sm utility should be applied"

    # Test shadow
    soup = cotton_render_soup(
        "info-box",
        icon="box-seam",
        text="Shadow",
        number="200",
        **{"class": "shadow"},
    )
    info_box = soup.find("div", class_="info-box")
    assert "shadow" in info_box.get("class"), "shadow utility should be applied"

    # Test shadow-lg
    soup_lg = cotton_render_soup(
        "info-box",
        icon="box-seam",
        text="Shadow Large",
        number="300",
        **{"class": "shadow-lg"},
    )
    info_box_lg = soup_lg.find("div", class_="info-box")
    assert "shadow-lg" in info_box_lg.get("class"), "shadow-lg utility should be applied"


@pytest.mark.django_db
def test_info_box_all_variant_colors(cotton_render_soup):
    """Test info box with all Bootstrap variant colors (T067) - default fill='icon' mode."""
    variants = ["primary", "success", "warning", "danger", "info", "secondary"]

    for variant in variants:
        soup = cotton_render_soup(
            "info-box",
            icon="box-seam",
            text=f"Test {variant}",
            number="100",
            variant=variant,
        )
        info_box = soup.find("div", class_="info-box")

        # With fill="icon" (default), variant class should be on icon span
        icon_span = info_box.find("span", class_="info-box-icon")
        assert icon_span is not None, f"Icon span should exist for variant={variant}"

        icon_classes = icon_span.get("class")
        expected_class = f"text-bg-{variant}"
        assert (
            expected_class in icon_classes
        ), f"{expected_class} class should be applied to icon span for variant={variant}"
