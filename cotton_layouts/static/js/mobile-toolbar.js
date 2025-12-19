// Detail View JavaScript Functionality
// Handles sidebar toggle and mobile toolbar scroll behavior

(function () {
  'use strict'

  // Mobile toolbar scroll behavior
  function initMobileToolbarScroll() {
    const toolbar = document.querySelector('.mobile-toolbar.sticky')
    if (!toolbar) return

    let lastScrollTop = 0
    let ticking = false
    let isScrolling = false
    let scrollTimeout

    // Add animated class for smooth transitions
    toolbar.classList.add('animated')

    function updateToolbarVisibility() {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop
      const scrollDelta = currentScrollTop - lastScrollTop

      // Clear previous scroll timeout
      clearTimeout(scrollTimeout)

      // Determine scroll direction and visibility
      if (currentScrollTop <= 0) {
        // At top of page - show toolbar
        toolbar.classList.add('show')
      } else if (scrollDelta > 0 && currentScrollTop > 100) {
        // Scrolling down and not at top - hide toolbar
        toolbar.classList.remove('show')
      } else if (scrollDelta < 0) {
        // Scrolling up - show toolbar
        toolbar.classList.add('show')
      }

      // Set timeout to show toolbar when scrolling stops
      isScrolling = true
      scrollTimeout = setTimeout(function () {
        isScrolling = false
        // Show toolbar when user stops scrolling (unless they're at the very bottom)
        if (currentScrollTop > 0 && (window.innerHeight + currentScrollTop) < document.documentElement.scrollHeight - 50) {
          toolbar.classList.add('show')
        }
      }, 150)

      lastScrollTop = currentScrollTop
      ticking = false
    }

    function requestTick() {
      if (!ticking) {
        requestAnimationFrame(updateToolbarVisibility)
        ticking = true
      }
    }

    // Listen for scroll events
    window.addEventListener('scroll', requestTick, { passive: true })

    // Initially show the toolbar
    toolbar.classList.add('show')
  }

  // Initialize all functionality when DOM is ready
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        initMobileToolbarScroll()
      })
    } else {
      initMobileToolbarScroll()
    }
  }

  // Start initialization
  init()
})()