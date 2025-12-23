/**
 * Content Sidebars JavaScript
 * Handles collapsible left and right sidebars within content areas
 * Uses namespaced localStorage for independent state management
 */

(function () {
  'use strict'

  // Storage keys for independent state
  const STORAGE_KEY_LEFT = 'contentSidebarLeftCollapsed'
  const STORAGE_KEY_RIGHT = 'contentSidebarRightCollapsed'

  /**
   * Save sidebar collapsed state to localStorage
   */
  function saveState(key, isCollapsed) {
    try {
      localStorage.setItem(key, isCollapsed.toString())
    } catch (e) {
      console.warn('Failed to save content layout state:', e)
    }
  }

  /**
   * Get sidebar collapsed state from localStorage
   */
  function getState(key) {
    try {
      return localStorage.getItem(key) === 'true'
    } catch (e) {
      return false
    }
  }

  /**
   * Restore sidebar state WITHOUT animation on page load
   */
  function restoreSidebarState(sidebar, storageKey) {
    const isCollapsed = getState(storageKey)

    if (isCollapsed) {
      // Disable transitions temporarily
      sidebar.style.transition = 'none'
      sidebar.classList.add('collapsed')

      // Force reflow
      sidebar.offsetHeight

      // Re-enable transitions after a frame
      requestAnimationFrame(() => {
        sidebar.style.transition = ''
      })
    }
  }

  /**
   * Toggle sidebar collapsed state
   */
  function toggleSidebar(sidebar, storageKey) {
    sidebar.classList.toggle('collapsed')
    const isCollapsed = sidebar.classList.contains('collapsed')
    saveState(storageKey, isCollapsed)
  }

  /**
   * Initialize left sidebar collapse functionality
   */
  function initLeftSidebars() {
    const sidebars = document.querySelectorAll('.content-sidebar-left[data-collapsible="True"]')

    sidebars.forEach(sidebar => {
      // Restore state on load
      restoreSidebarState(sidebar, STORAGE_KEY_LEFT)

      // Find toggle button within this sidebar
      const toggleButton = sidebar.querySelector('.content-sidebar-toggle-left')

      if (toggleButton) {
        toggleButton.addEventListener('click', (e) => {
          e.preventDefault()
          e.stopPropagation()
          toggleSidebar(sidebar, STORAGE_KEY_LEFT)
        })
      }
    })
  }

  /**
   * Initialize right sidebar collapse functionality
   */
  function initRightSidebars() {
    const sidebars = document.querySelectorAll('.content-sidebar-right[data-collapsible="True"]')

    sidebars.forEach(sidebar => {
      // Restore state on load
      restoreSidebarState(sidebar, STORAGE_KEY_RIGHT)

      // Find toggle button within this sidebar
      const toggleButton = sidebar.querySelector('.content-sidebar-toggle-right')

      if (toggleButton) {
        toggleButton.addEventListener('click', (e) => {
          e.preventDefault()
          e.stopPropagation()
          toggleSidebar(sidebar, STORAGE_KEY_RIGHT)
        })
      }
    })
  }

  /**
   * Initialize on DOM ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initLeftSidebars()
      initRightSidebars()
    })
  } else {
    initLeftSidebars()
    initRightSidebars()
  }

})()
