/**
 * InnerLayoutManager - Manages collapsible sidebar behavior in the inner layout
 *
 * Features:
 * - Toggle collapse state for primary and secondary sidebars
 * - Persist collapse state to localStorage
 * - Handle responsive behavior (disable collapse in offcanvas mode)
 * - Emit custom events for state changes
 * - Keyboard navigation support
 */

(function () {
  'use strict'

  class InnerLayoutManager {
    constructor (options) {
      options = options || {}
      this.primarySidebar = document.getElementById('primary-sidebar')
      this.secondarySidebar = document.getElementById('secondary-sidebar')
      this.breakpoint = options.breakpoint || 'md'
      this.primaryCollapsed = options.primaryCollapsed || false
      this.secondaryCollapsed = options.secondaryCollapsed || false
    }

    /**
     * Initialize the inner layout manager
     * Sets up event listeners and restores state from localStorage
     */
    init() {
      // Restore state from localStorage
      const storedPrimaryState = localStorage.getItem('innerlayout_primary_collapsed')
      if (storedPrimaryState !== null) {
        this.primaryCollapsed = storedPrimaryState === 'true'
      }

      const storedSecondaryState = localStorage.getItem('innerlayout_secondary_collapsed')
      if (storedSecondaryState !== null) {
        this.secondaryCollapsed = storedSecondaryState === 'true'
      }

      // Apply initial states (without animation)
      if (this.primarySidebar && this.primaryCollapsed && !this.isOffcanvasMode()) {
        this.primarySidebar.style.transition = 'none'
        this.primarySidebar.classList.add('collapsed')
        // Force reflow then re-enable transitions
        this.primarySidebar.offsetHeight
        this.primarySidebar.style.transition = ''
      }

      if (this.secondarySidebar && this.secondaryCollapsed && !this.isOffcanvasMode()) {
        this.secondarySidebar.style.transition = 'none'
        this.secondarySidebar.classList.add('collapsed')
        // Force reflow then re-enable transitions
        this.secondarySidebar.offsetHeight
        this.secondarySidebar.style.transition = ''
      }

      // Set up event listeners
      this.setupEventListeners()

      // Emit init event
      this.emitEvent('innerlayout:initialized')
    }

    /**
     * Set up event listeners for collapse toggles and window resize
     */
    setupEventListeners() {
      const self = this

      // Collapse toggle buttons
      const collapseToggles = document.querySelectorAll('.collapse-toggle')
      collapseToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
          e.preventDefault()
          e.stopPropagation()

          const target = this.getAttribute('data-target')
          if (target === 'primary-sidebar') {
            self.toggleCollapse('primary')
          } else if (target === 'secondary-sidebar') {
            self.toggleCollapse('secondary')
          }
        })
      })

      // Window resize listener
      window.addEventListener('resize', function () {
        self.handleResize()
      })

      // Bootstrap offcanvas events
      if (this.primarySidebar) {
        this.primarySidebar.addEventListener('shown.bs.offcanvas', function () {
          self.emitEvent('innerlayout:offcanvasmode', { sidebar: 'primary', shown: true })
        })

        this.primarySidebar.addEventListener('hidden.bs.offcanvas', function () {
          self.emitEvent('innerlayout:offcanvasmode', { sidebar: 'primary', shown: false })
        })
      }

      if (this.secondarySidebar) {
        this.secondarySidebar.addEventListener('shown.bs.offcanvas', function () {
          self.emitEvent('innerlayout:offcanvasmode', { sidebar: 'secondary', shown: true })
        })

        this.secondarySidebar.addEventListener('hidden.bs.offcanvas', function () {
          self.emitEvent('innerlayout:offcanvasmode', { sidebar: 'secondary', shown: false })
        })
      }
    }

    /**
     * Toggle collapse state for a sidebar
     * @param {string} sidebar - Which sidebar to toggle ('primary' or 'secondary')
     */
    toggleCollapse(sidebar) {
      // Cannot collapse in offcanvas mode
      if (this.isOffcanvasMode()) {
        console.warn('Cannot collapse sidebar in offcanvas mode')
        return
      }

      const element = sidebar === 'primary' ? this.primarySidebar : this.secondarySidebar
      if (!element) return

      const isCollapsed = element.classList.contains('collapsed')
      const newState = !isCollapsed

      if (newState) {
        element.classList.add('collapsed')
        this.emitEvent('innerlayout:collapsed', { sidebar: sidebar })
      } else {
        element.classList.remove('collapsed')
        this.emitEvent('innerlayout:expanded', { sidebar: sidebar })
      }

      // Update internal state
      if (sidebar === 'primary') {
        this.primaryCollapsed = newState
        localStorage.setItem('innerlayout_primary_collapsed', String(newState))
      } else {
        this.secondaryCollapsed = newState
        localStorage.setItem('innerlayout_secondary_collapsed', String(newState))
      }
    }

    /**
     * Check if a sidebar is currently collapsed
     * @param {string} sidebar - Which sidebar to check ('primary' or 'secondary')
     * @returns {boolean} true if collapsed, false otherwise
     */
    isCollapsed(sidebar) {
      const element = sidebar === 'primary' ? this.primarySidebar : this.secondarySidebar
      return element ? element.classList.contains('collapsed') : false
    }

    /**
     * Check if viewport is in offcanvas mode (below breakpoint)
     * @returns {boolean} true if in offcanvas mode, false otherwise
     */
    isOffcanvasMode() {
      const breakpointMap = {
        sm: 576,
        md: 768,
        lg: 992,
        xl: 1200,
        xxl: 1400
      }

      const breakpointPx = breakpointMap[this.breakpoint] || 768
      return window.innerWidth < breakpointPx
    }

    /**
     * Handle window resize events
     * Removes collapsed state if entering offcanvas mode
     */
    handleResize() {
      if (this.isOffcanvasMode()) {
        // Remove collapsed state in offcanvas mode
        if (this.primarySidebar && this.primarySidebar.classList.contains('collapsed')) {
          this.primarySidebar.classList.remove('collapsed')
        }
        if (this.secondarySidebar && this.secondarySidebar.classList.contains('collapsed')) {
          this.secondarySidebar.classList.remove('collapsed')
        }
      } else {
        // Restore collapsed state from stored values
        if (this.primarySidebar && this.primaryCollapsed) {
          this.primarySidebar.classList.add('collapsed')
        }
        if (this.secondarySidebar && this.secondaryCollapsed) {
          this.secondarySidebar.classList.add('collapsed')
        }
      }
    }

    /**
     * Emit a custom event
     * @param {string} eventName - Name of the event
     * @param {Object} detail - Event detail data
     */
    emitEvent(eventName, detail) {
      detail = detail || {}
      const event = new CustomEvent(eventName, { detail: detail, bubbles: true })
      document.dispatchEvent(event)
    }
  }

  // Auto-initialize on DOMContentLoaded
  function initInnerLayout() {
    // Check if any collapsible sidebars exist
    const hasCollapsible = document.querySelector('.collapsible')
    if (hasCollapsible) {
      const contentShell = document.querySelector('.content-shell')
      const breakpoint = contentShell ? contentShell.getAttribute('data-breakpoint') : 'md'

      const manager = new InnerLayoutManager({ breakpoint: breakpoint })
      manager.init()

      // Expose to window for external access
      window.innerLayoutManager = manager
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInnerLayout)
  } else {
    initInnerLayout()
  }

  // Export for module usage
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = InnerLayoutManager
  }

})()
