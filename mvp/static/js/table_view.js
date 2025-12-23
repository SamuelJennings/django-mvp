/**
 * Table View JavaScript - Mobile search drawer and responsive functionality
 */

// Mobile Search Drawer Functions
function toggleSearchDrawer() {
  const drawer = document.getElementById('searchDrawer')
  drawer.classList.toggle('show')

  // Focus on the search input when drawer opens
  if (drawer.classList.contains('show')) {
    const searchInput = drawer.querySelector('input[type="text"]')
    setTimeout(() => searchInput.focus(), 100)
  }
}

// Clear all filters function
function clearAllFilters() {
  const form = document.getElementById('filterForm')
  if (form) {
    // Reset all form fields except hidden fields
    const inputs = form.querySelectorAll('input:not([type="hidden"]), select, textarea')
    inputs.forEach(input => {
      if (input.type === 'checkbox' || input.type === 'radio') {
        input.checked = false
      } else {
        input.value = ''
      }
    })
    // Submit the form to show all results
    form.submit()
  }
}

// Synchronize search field between main toolbar and hidden filter form
function syncSearchFields() {
  // Get all search input fields
  const searchFields = document.querySelectorAll('input[name="search"]')

  if (searchFields.length > 0) {
    searchFields.forEach(field => {
      field.addEventListener('input', function () {
        // Update all search fields with the same value
        searchFields.forEach(otherField => {
          if (otherField !== field) {
            otherField.value = field.value
          }
        })

        // Update the hidden field in filter form
        const hiddenSearch = document.getElementById('search-hidden')
        if (hiddenSearch) {
          hiddenSearch.value = field.value
        }
      })
    })
  }
}

// Toggle fullscreen mode for the table view
function toggleFullscreen() {
  const mainLayout = document.querySelector('.main-layout')
  const fullscreenIcons = document.querySelectorAll('#fullscreenIcon, #fullscreenIconMobile')

  if (mainLayout) {
    mainLayout.classList.toggle('fullscreen-mode')

    // Update icon - toggle between fullscreen and fullscreen_exit
    const isFullscreen = mainLayout.classList.contains('fullscreen-mode')
    fullscreenIcons.forEach(icon => {
      icon.setAttribute('name', isFullscreen ? 'fullscreen_exit' : 'fullscreen')
    })
  }
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
  // Sync search fields
  syncSearchFields()

  // Close drawer when clicking outside
  document.addEventListener('click', function (event) {
    const drawer = document.getElementById('searchDrawer')
    const searchButton = document.querySelector('.mobile-controls button[onclick="toggleSearchDrawer()"]')

    if (drawer && drawer.classList.contains('show') &&
      !drawer.contains(event.target) &&
      searchButton && !searchButton.contains(event.target)) {
      drawer.classList.remove('show')
    }
  })

  // Close drawer on escape key
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      const drawer = document.getElementById('searchDrawer')
      if (drawer) {
        drawer.classList.remove('show')
      }

      // Also close offcanvas
      const offcanvas = document.getElementById('filterOffcanvas')
      if (offcanvas && offcanvas.classList.contains('show')) {
        const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas)
        if (bsOffcanvas) {
          bsOffcanvas.hide()
        }
      }
    }
  })

  // Optional: Initialize select all checkbox functionality
  const selectAllCheckbox = document.getElementById('selectAll')
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', function () {
      const rowCheckboxes = document.querySelectorAll('.table-container tbody input[type="checkbox"]')
      rowCheckboxes.forEach(checkbox => {
        checkbox.checked = this.checked
      })
    })
  }

  // Optional: Update select all when individual checkboxes change
  const rowCheckboxes = document.querySelectorAll('.table-container tbody input[type="checkbox"]')
  rowCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const allCheckboxes = document.querySelectorAll('.table-container tbody input[type="checkbox"]')
      const checkedCheckboxes = document.querySelectorAll('.table-container tbody input[type="checkbox"]:checked')
      const selectAllCheckbox = document.getElementById('selectAll')

      if (selectAllCheckbox) {
        if (checkedCheckboxes.length === 0) {
          selectAllCheckbox.indeterminate = false
          selectAllCheckbox.checked = false
        } else if (checkedCheckboxes.length === allCheckboxes.length) {
          selectAllCheckbox.indeterminate = false
          selectAllCheckbox.checked = true
        } else {
          selectAllCheckbox.indeterminate = true
        }
      }
    })
  })
})