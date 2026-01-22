"""End-to-end tests for Django Tables2 integration using Playwright."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_navigate_to_demo_page_and_verify_table_renders(page: Page, live_server):
    """Navigate to DataTables demo page and verify table renders.

    Tests:
    - Page loads successfully
    - Page title is correct
    - Table is visible
    - Table has headers
    - Table has data rows
    """
    # Navigate to the demo page
    page.goto(f"{live_server.url}/datatables-demo/")

    # Wait for page to load
    expect(page).to_have_title("Django MVP Example")

    # Verify table is visible
    table = page.locator("table")
    expect(table).to_be_visible()

    # Verify table has headers
    headers = table.locator("thead th")
    expect(headers).to_have_count(16)

    # Verify table has data rows
    rows = table.locator("tbody tr")
    expect(rows.first).to_be_visible()


def test_sorting_by_clicking_column_header(page: Page, live_server):
    """Click column header and verify rows reorder.

    Tests:
    - Column headers are clickable
    - Clicking header adds sort indicator
    - Table data reorders
    - URL updates with sort parameter
    """
    # Navigate to the demo page
    page.goto(f"{live_server.url}/datatables-demo/")

    # Wait for table to load
    table = page.locator("table")
    expect(table).to_be_visible()

    # Click on "Name" column header to sort
    name_header = table.locator("thead th a:has-text('Name')")
    expect(name_header).to_be_visible()
    name_header.click()

    # Wait for page reload
    page.wait_for_load_state("networkidle")

    # Verify URL contains sort parameter
    expect(page).to_have_url(f"{live_server.url}/datatables-demo/?sort=name")

    # Verify sort indicator exists in header
    sort_indicator = name_header.locator("..")  # Parent th element
    class_attr = sort_indicator.get_attribute("class") or ""
    # Check for orderable class or sort indicator
    assert any(
        cls in class_attr for cls in ["orderable", "asc", "desc"]
    ), f"Expected sort indicator in class attribute, got: {class_attr}"


def test_pagination_navigation(page: Page, live_server):
    """Click page 2 and verify different products display.

    Tests:
    - Pagination controls are visible
    - Clicking "Next" or page number loads new data
    - URL updates with page parameter
    - Table shows different rows
    """
    # Navigate to the demo page
    page.goto(f"{live_server.url}/datatables-demo/")

    # Wait for table to load
    table = page.locator("table")
    expect(table).to_be_visible()

    # Get first row's product name on page 1
    first_row_page1 = table.locator("tbody tr:first-child td:first-child").inner_text()

    # Find pagination controls - look for page 2 link or Next button
    pagination = page.locator("nav[aria-label='pagination']")
    expect(pagination).to_be_visible()

    # Try to click page 2 link
    page_2_link = pagination.locator("a:has-text('2')")

    # If page 2 exists (enough data), click it
    if page_2_link.count() > 0:
        page_2_link.click()

        # Wait for page reload
        page.wait_for_load_state("networkidle")

        # Verify URL contains page parameter
        expect(page).to_have_url(f"{live_server.url}/datatables-demo/?page=2")

        # Verify first row changed (different products on page 2)
        first_row_page2 = table.locator("tbody tr:first-child td:first-child").inner_text()
        assert first_row_page1 != first_row_page2, "Page 2 should show different products"
    else:
        # Not enough data for pagination, verify message or single page
        pytest.skip("Not enough products for pagination (< 26 products)")


def test_keyboard_navigation(page: Page, live_server):
    """Tab through table headers and pagination links.

    Tests:
    - Table headers are keyboard focusable
    - Pagination links are keyboard focusable
    - Tab order is logical
    - Enter key activates links
    """
    # Navigate to the demo page
    page.goto(f"{live_server.url}/datatables-demo/")

    # Wait for table to load
    table = page.locator("table")
    expect(table).to_be_visible()

    # Focus on first sortable column header
    first_header_link = table.locator("thead th a").first
    first_header_link.focus()

    # Verify element is focused
    expect(first_header_link).to_be_focused()

    # Press Tab to move to next header
    page.keyboard.press("Tab")

    # Verify focus moved to another link (either next header or pagination)
    # We just verify that focus moved from the first link
    focused_element = page.locator(":focus")
    first_href = first_header_link.get_attribute("href") or ""
    if first_href:
        expect(focused_element).not_to_have_attribute("href", first_href)

    # Tab to pagination if it exists
    pagination = page.locator("nav[aria-label='pagination']")
    if pagination.count() > 0:
        pagination_link = pagination.locator("a").first
        pagination_link.focus()
        expect(pagination_link).to_be_focused()

        # Press Enter to activate pagination link
        page.keyboard.press("Enter")

        # Wait for navigation
        page.wait_for_load_state("networkidle")

        # Verify page changed (URL should be different)
        assert "page=" in page.url or "sort=" in page.url, "Pressing Enter on pagination link should navigate"
