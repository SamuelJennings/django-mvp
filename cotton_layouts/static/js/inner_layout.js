/**
 * Inner Layout JavaScript
 * Handles collapsible primary and secondary sidebars within content areas
 * Uses namespaced localStorage for independent state management
 */

(function () {
  'use strict'

  // Storage keys for independent state
  const STORAGE_KEY_PRIMARY = 'innerPrimaryCollapsed'
  const STORAGE_KEY_SECONDARY = 'innerSecondaryCollapsed'

  /**
   * Save sidebar collapsed state to localStorage
   */
  function saveState(key, isCollapsed) {
    try {
      localStorage.setItem(key, isCollapsed.toString())
    } catch (e) {
      console.warn('Failed to save inner layout state:', e)
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
   * Initialize primary sidebar collapse functionality
   */
  function initPrimarySidebars() {
    const sidebars = document.querySelectorAll('.inner-primary[data-collapsible="True"]')

    sidebars.forEach(sidebar => {
      // Restore state on load
      restoreSidebarState(sidebar, STORAGE_KEY_PRIMARY)

      // Find toggle button within this sidebar
      const toggleButton = sidebar.querySelector('.inner-primary-toggle')

      if (toggleButton) {
        toggleButton.addEventListener('click', (e) => {
          e.preventDefault()
          e.stopPropagation()
          toggleSidebar(sidebar, STORAGE_KEY_PRIMARY)
        })
      }
    })
  }

  /**
   * Initialize secondary sidebar collapse functionality
   */
  function initSecondarySidebars() {
    const sidebars = document.querySelectorAll('.inner-secondary[data-collapsible="True"]')

    sidebars.forEach(sidebar => {
      // Restore state on load
      restoreSidebarState(sidebar, STORAGE_KEY_SECONDARY)

      // Find toggle button within this sidebar
      const toggleButton = sidebar.querySelector('.inner-secondary-toggle')

      if (toggleButton) {
        toggleButton.addEventListener('click', (e) => {
          e.preventDefault()
          e.stopPropagation()
          toggleSidebar(sidebar, STORAGE_KEY_SECONDARY)
        })
      }
    })
  }

  /**
   * Initialize on DOM ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initPrimarySidebars()
      initSecondarySidebars()
    })
  } else {
    initPrimarySidebars()
    initSecondarySidebars()
  }

})()
