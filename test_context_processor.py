#!/usr/bin/env python
"""Quick test of context processor functionality."""

import os
import sys

# Setup Django
os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
sys.path.insert(0, ".")

import django

django.setup()

from mvp.context_processors import _process_page_config

print("=" * 60)
print("Testing Context Processor Defaults")
print("=" * 60)

# Test 1: Empty config gets defaults
print("\n✓ Test 1: Empty config → defaults applied")
result = _process_page_config({})
assert result["brand"]["text"] == "Django MVP", f"Expected 'Django MVP', got {result['brand']['text']}"
assert result["sidebar"]["show_at"] is False, f"Expected False, got {result['sidebar']['show_at']}"
assert result["sidebar"]["collapsible"] is True, f"Expected True, got {result['sidebar']['collapsible']}"
assert result["navbar"]["menu_visible_at"] == "sm", f"Expected 'sm', got {result['navbar']['menu_visible_at']}"
assert result["actions"] == [], f"Expected [], got {result['actions']}"
print("  - brand.text = Django MVP ✓")
print("  - sidebar.show_at = False ✓")
print("  - sidebar.collapsible = True ✓")
print("  - navbar.menu_visible_at = sm ✓")
print("  - actions = [] ✓")

# Test 2: Sidebar in-flow disables navbar menu
print("\n✓ Test 2: Sidebar in-flow → navbar menu disabled")
result2 = _process_page_config(
    {
        "sidebar": {"show_at": "lg"},
        "navbar": {"menu_visible_at": "sm"},
    }
)
assert result2["navbar"]["menu_visible_at"] is False, f"Expected False, got {result2['navbar']['menu_visible_at']}"
print("  - navbar.menu_visible_at = False (enforced) ✓")

# Test 3: Navbar-only allows menu
print("\n✓ Test 3: Navbar-only mode → menu allowed")
result3 = _process_page_config(
    {
        "sidebar": {"show_at": False},
        "navbar": {"menu_visible_at": "lg"},
    }
)
assert result3["navbar"]["menu_visible_at"] == "lg", f"Expected 'lg', got {result3['navbar']['menu_visible_at']}"
print("  - navbar.menu_visible_at = lg (allowed) ✓")

# Test 4: Invalid breakpoint falls back
print("\n✓ Test 4: Invalid breakpoint → safe fallback")
result4 = _process_page_config(
    {
        "sidebar": {"show_at": "invalid"},
        "navbar": {"menu_visible_at": "xlarge"},
    }
)
assert result4["sidebar"]["show_at"] is False, f"Expected False, got {result4['sidebar']['show_at']}"
assert result4["navbar"]["menu_visible_at"] == "sm", f"Expected 'sm', got {result4['navbar']['menu_visible_at']}"
print("  - sidebar.show_at = False (fallback) ✓")
print("  - navbar.menu_visible_at = sm (fallback) ✓")

print("\n" + "=" * 60)
print("All Context Processor Tests Passed! ✓")
print("=" * 60)
