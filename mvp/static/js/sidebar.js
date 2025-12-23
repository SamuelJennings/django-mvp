(function () {
  'use strict'

  const SIDEBAR_STATE_KEY = 'sidebarCollapsed'

  // Get layout mode from body classes
  function getLayoutMode() {
    const body = document.body
    if (body.classList.contains('layout-navbar')) return 'navbar'
    if (body.classList.contains('layout-both')) return 'both'
    if (body.classList.contains('layout-sidebar')) return 'sidebar'
    return 'sidebar' // default
  }

  // Get toggle breakpoint from .app-shell classes
  function getToggleBreakpoint() {
    const appShell = document.querySelector('.app-shell')
    if (!appShell) return 'lg' // default if no app-shell found

    const breakpoints = ['sm', 'md', 'lg', 'xl', 'xxl']
    for (const bp of breakpoints) {
      if (appShell.classList.contains('hide-sidebar-' + bp)) {
        return bp
      }
    }
    return 'lg' // default
  }

  // Check if sidebar is in-flow (vs offcanvas) at current window width
  function isSidebarInFlow() {
    const layoutMode = getLayoutMode()

    // In navbar-only mode, sidebar is never in-flow (always offcanvas)
    if (layoutMode === 'navbar') return false

    const breakpoint = getToggleBreakpoint()
    const breakpointWidths = {
      'sm': 576,
      'md': 768,
      'lg': 992,
      'xl': 1200,
      'xxl': 1400
    }

    const minWidth = breakpointWidths[breakpoint] || 992
    return window.innerWidth >= minWidth
  }

  // Restore sidebar state from localStorage without animation
  function restoreSidebarState() {
    const sidebarContainers = document.querySelectorAll('.sidebar-main')
    const isCollapsed = localStorage.getItem(SIDEBAR_STATE_KEY) === 'true'

    sidebarContainers.forEach(function (container) {
      // Find the actual .sidebar component inside the wrapper
      const sidebar = container.querySelector('.sidebar')
      if (!sidebar) return

      // Only apply collapsed state if sidebar is in-flow and collapsible
      if (isCollapsed && isSidebarInFlow() && container.classList.contains('collapsible')) {
        // Temporarily disable transitions to prevent animation on page load
        sidebar.style.transition = 'none'
        sidebar.classList.add('collapsed')

        // Force a reflow to ensure the transition is disabled
        sidebar.offsetHeight

        // Re-enable transitions after a brief delay
        requestAnimationFrame(function () {
          sidebar.style.transition = ''
        })
      } else {
        sidebar.classList.remove('collapsed')
      }
    })
  }

  // Save sidebar state to localStorage
  function saveSidebarState(isCollapsed) {
    localStorage.setItem(SIDEBAR_STATE_KEY, isCollapsed.toString())
  }

  // Sidebar toggle functionality
  function initSidebarToggle() {
    // Find all sidebar toggle buttons
    const toggleButtons = document.querySelectorAll('.sidebar-toggle')

    toggleButtons.forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault()

        // Find the nearest .sidebar component (not the wrapper)
        const sidebar = button.closest('.sidebar')

        if (sidebar) {
          // Only allow collapse/expand when sidebar is in-flow
          if (!isSidebarInFlow()) {
            return // Ignore toggle when sidebar is in offcanvas mode
          }

          sidebar.classList.toggle('collapsed')

          // Save the new state
          const isCollapsed = sidebar.classList.contains('collapsed')
          saveSidebarState(isCollapsed)
        }
      })
    })
  }

  // Handle window resize - restore state when sidebar becomes in-flow
  function handleResize() {
    if (isSidebarInFlow()) {
      restoreSidebarState()
    } else {
      // Remove collapsed class when sidebar is offcanvas
      const sidebars = document.querySelectorAll('.sidebar-main')
      sidebars.forEach(function (sidebar) {
        sidebar.classList.remove('collapsed')
      })
    }
  }

  // Sync theme toggle in dropdown with main theme toggle
  function initThemeToggleDropdown() {
    const themeToggleDropdown = document.getElementById('themeToggleDropdown')
    const mainThemeToggle = document.getElementById('themeToggle')

    if (themeToggleDropdown && mainThemeToggle) {
      themeToggleDropdown.addEventListener('click', function (e) {
        e.preventDefault()
        mainThemeToggle.click()
      })
    }
  }

  // Initialize all functionality when DOM is ready
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        restoreSidebarState()
        initSidebarToggle()
        initThemeToggleDropdown()

        // Add resize listener with debounce
        let resizeTimeout
        window.addEventListener('resize', function () {
          clearTimeout(resizeTimeout)
          resizeTimeout = setTimeout(handleResize, 150)
        })
      })
    } else {
      restoreSidebarState()
      initSidebarToggle()
      initThemeToggleDropdown()

      // Add resize listener with debounce
      let resizeTimeout
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimeout)
        resizeTimeout = setTimeout(handleResize, 150)
      })
    }
  }

  // Start initialization
  init()
})()