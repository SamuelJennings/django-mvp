// Theme toggle functionality
function toggleTheme() {
  const html = document.documentElement
  const currentTheme = html.getAttribute('data-bs-theme')
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'

  html.setAttribute('data-bs-theme', newTheme)

  // Update icons
  const desktopIcon = document.getElementById('themeIcon')
  const mobileIcon = document.getElementById('mobileThemeIcon')

  if (newTheme === 'dark') {
    desktopIcon.className = 'bi bi-moon-fill'
    mobileIcon.className = 'bi bi-moon-fill me-2'
  } else {
    desktopIcon.className = 'bi bi-sun-fill'
    mobileIcon.className = 'bi bi-sun-fill me-2'
  }

  // Store preference
  localStorage.setItem('theme', newTheme)
}

// Initialize theme from localStorage
document.addEventListener('DOMContentLoaded', function () {
  const savedTheme = localStorage.getItem('theme') || 'light'
  document.documentElement.setAttribute('data-bs-theme', savedTheme)

  const desktopIcon = document.getElementById('themeIcon')
  const mobileIcon = document.getElementById('mobileThemeIcon')

  if (desktopIcon && savedTheme === 'dark') {
    desktopIcon.className = 'bi bi-moon-fill'
  }

  if (mobileIcon && savedTheme === 'dark') {
    mobileIcon.className = 'bi bi-moon-fill me-2'
  }

  // Add event listeners
  const themeToggle = document.getElementById('themeToggle')
  const mobileThemeToggle = document.getElementById('mobileThemeToggle')

  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme)
  }

  if (mobileThemeToggle) {
    mobileThemeToggle.addEventListener('click', toggleTheme)
  }

  // Close mobile menu when clicking on actual navigation links (not collapse toggles)
  document.querySelectorAll('#page-sidebar .nav-link:not([data-bs-toggle="collapse"])').forEach(link => {
    link.addEventListener('click', (e) => {
      // Only close if it's an actual navigation link with href, not a collapse toggle
      if (link.getAttribute('href') && link.getAttribute('href') !== '#') {
        const offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('page-sidebar'))
        if (offcanvas) {
          offcanvas.hide()
        }
      }
    })
  })

  // Initialize collapsible search
  initCollapsibleSearch()

  // Initialize modal search auto-focus
  initModalSearch()
})

// Modal search functionality
function initModalSearch() {
  const searchModal = document.getElementById('searchModal')

  if (searchModal) {
    searchModal.addEventListener('shown.bs.modal', function () {
      const searchInput = document.getElementById('searchModalInput')
      if (searchInput) {
        searchInput.focus()
      }
    })
  }
}

// Collapsible search functionality
function initCollapsibleSearch() {
  const searchContainers = document.querySelectorAll('.navbar-search-collapsible')

  searchContainers.forEach(container => {
    const toggle = container.querySelector('.navbar-search-toggle')
    const form = container.querySelector('.navbar-search-form')
    const input = form?.querySelector('input[type="search"]')

    if (!toggle || !form) return

    // Toggle search expand/collapse
    toggle.addEventListener('click', function (e) {
      e.preventDefault()
      e.stopPropagation()

      const isCollapsed = form.classList.contains('collapsed')

      if (isCollapsed) {
        form.classList.remove('collapsed')
        form.classList.add('expanded')
        // Focus input after animation
        setTimeout(() => input?.focus(), 300)
      } else {
        form.classList.add('collapsed')
        form.classList.remove('expanded')
        input?.blur()
      }
    })

    // Close search when clicking outside
    document.addEventListener('click', function (e) {
      if (!container.contains(e.target) && form.classList.contains('expanded')) {
        form.classList.add('collapsed')
        form.classList.remove('expanded')
        input?.blur()
      }
    })

    // Prevent closing when clicking inside the form
    form.addEventListener('click', function (e) {
      e.stopPropagation()
    })
  })
}
