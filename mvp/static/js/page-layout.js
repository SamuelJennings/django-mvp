/**
 * Inner Layout System - JavaScript
 *
 * Handles sidebar toggle functionality, session persistence, and ARIA state management
 * for the inner layout component system.
 *
 * Features:
 * - Sidebar collapse/expand toggle
 * - Session storage persistence
 * - ARIA state updates for accessibility
 * - Mobile overlay click-to-close
 * - Keyboard navigation support
 */

(function () {
  "use strict"

  // Storage key for sidebar state persistence
  const STORAGE_KEY = "innerLayoutSidebarCollapsed"

  // =============================================================================
  // Initialize
  // =============================================================================

  /**
   * Initialize inner layout functionality when DOM is ready
   */
  function init() {
    // Find all inner layout containers
    const innerLayouts = document.querySelectorAll(".page-layout")

    innerLayouts.forEach((layout) => {
      initializeSidebarToggle(layout)
      restoreSidebarState(layout)
    })
  }

  // =============================================================================
  // Sidebar Toggle
  // =============================================================================

  /**
   * Initialize sidebar toggle functionality for a layout
   * @param {HTMLElement} layout - The inner layout container
   */
  function initializeSidebarToggle(layout) {
    const sidebar = layout.querySelector(".page-sidebar")
    const toggleButton = layout.querySelector('[data-action="toggle-sidebar"]')

    if (!sidebar || !toggleButton) {
      return // No sidebar or toggle button found
    }

    // Set initial ARIA states
    updateAriaStates(toggleButton, sidebar)

    // Toggle button click handler
    toggleButton.addEventListener("click", (event) => {
      event.preventDefault()
      toggleSidebar(sidebar, toggleButton)
    })

    // Backdrop click handler (mobile)
    layout.addEventListener("click", (event) => {
      if (event.target === layout && !sidebar.classList.contains("collapsed")) {
        const breakpoint = layout.dataset.sidebarBreakpoint || "lg"
        if (isBelowBreakpoint(breakpoint)) {
          toggleSidebar(sidebar, toggleButton)
        }
      }
    })

    // Keyboard support: Escape to close sidebar on mobile
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !sidebar.classList.contains("collapsed")) {
        const breakpoint = layout.dataset.sidebarBreakpoint || "lg"
        if (isBelowBreakpoint(breakpoint)) {
          toggleSidebar(sidebar, toggleButton)
        }
      }
    })
  }

  /**
   * Toggle sidebar collapsed state
   * @param {HTMLElement} sidebar - The sidebar element
   * @param {HTMLElement} toggleButton - The toggle button element
   */
  function toggleSidebar(sidebar, toggleButton) {
    const isCollapsed = sidebar.classList.toggle("collapsed")

    // Update ARIA states
    updateAriaStates(toggleButton, sidebar)

    // Persist state
    saveSidebarState(isCollapsed)

    // Dispatch custom event for other scripts to listen to
    sidebar.dispatchEvent(
      new CustomEvent("sidebarToggle", {
        bubbles: true,
        detail: { collapsed: isCollapsed },
      }),
    )
  }

  /**
   * Update ARIA attributes for accessibility
   * @param {HTMLElement} toggleButton - The toggle button element
   * @param {HTMLElement} sidebar - The sidebar element
   */
  function updateAriaStates(toggleButton, sidebar) {
    const isCollapsed = sidebar.classList.contains("collapsed")

    toggleButton.setAttribute("aria-expanded", !isCollapsed)
    sidebar.setAttribute("aria-hidden", isCollapsed)

    // Update button label
    const icon = toggleButton.querySelector("i")
    if (icon) {
      // Toggle icon classes if using bi-arrow-bar-left/right pattern
      if (isCollapsed) {
        icon.classList.remove("bi-arrow-bar-right")
        icon.classList.add("bi-arrow-bar-left")
        toggleButton.setAttribute("aria-label", "Expand sidebar")
      } else {
        icon.classList.remove("bi-arrow-bar-left")
        icon.classList.add("bi-arrow-bar-right")
        toggleButton.setAttribute("aria-label", "Collapse sidebar")
      }
    }
  }

  // =============================================================================
  // State Persistence
  // =============================================================================

  /**
   * Save sidebar collapsed state to session storage
   * @param {boolean} isCollapsed - Whether sidebar is collapsed
   */
  function saveSidebarState(isCollapsed) {
    try {
      sessionStorage.setItem(STORAGE_KEY, isCollapsed ? "1" : "0")

      // Sync with html data attribute for inline script on next page load
      if (isCollapsed) {
        document.documentElement.setAttribute(
          "data-page-sidebar-collapsed",
          "true",
        )
      } else {
        document.documentElement.removeAttribute("data-page-sidebar-collapsed")
      }
    } catch (e) {
      console.warn("Failed to save sidebar state:", e)
    }
  }

  /**
   * Restore sidebar state from session storage
   * @param {HTMLElement} layout - The inner layout container
   */
  function restoreSidebarState(layout) {
    try {
      const savedState = sessionStorage.getItem(STORAGE_KEY)
      const sidebar = layout.querySelector(".page-sidebar")
      const toggleButton = layout.querySelector(
        '[data-action="toggle-sidebar"]',
      )

      if (!sidebar) return

      // Check if state was already applied by inline script
      const preApplied = document.documentElement.hasAttribute(
        "data-page-sidebar-collapsed",
      )

      if (savedState === "1") {
        if (preApplied) {
          // State already applied via inline script - just add class for JS state tracking
          sidebar.classList.add("collapsed")
        } else if (!sidebar.classList.contains("collapsed")) {
          // Apply collapsed state now
          sidebar.classList.add("collapsed")
        }

        if (toggleButton) {
          updateAriaStates(toggleButton, sidebar)
        }
      }
    } catch (e) {
      console.warn("Failed to restore sidebar state:", e)
    }
  }

  // =============================================================================
  // Responsive Helpers
  // =============================================================================

  /**
   * Check if viewport is below a given breakpoint
   * @param {string} breakpoint - Bootstrap breakpoint name (sm, md, lg, xl, xxl)
   * @returns {boolean} - True if viewport is below breakpoint
   */
  function isBelowBreakpoint(breakpoint) {
    const breakpoints = {
      sm: 576,
      md: 768,
      lg: 992,
      xl: 1200,
      xxl: 1400,
    }

    const breakpointValue = breakpoints[breakpoint] || breakpoints.lg
    return window.innerWidth < breakpointValue
  }

  // =============================================================================
  // Auto-Initialize
  // =============================================================================

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init)
  } else {
    init()
  }

  // Re-initialize when content is dynamically loaded (e.g., HTMX, Turbo)
  document.addEventListener("htmx:afterSwap", init)
  document.addEventListener("turbo:load", init)

  // Export for manual initialization if needed
  window.innerLayout = {
    init: init,
  }
})()
