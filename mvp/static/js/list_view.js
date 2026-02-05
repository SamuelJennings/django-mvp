/**
 * FairDM List View JavaScript
 * Interactive functionality for list view page
 */

document.addEventListener('DOMContentLoaded', function () {
  initializeListView()
})

/**
 * Initialize list view functionality
 */
function initializeListView() {
  initializeTagFilters()
  initializeSearchFunctionality()
  initializeExpandButtons()
  initializeSortFunctionality()
  initializeFilterFunctionality()
  initializePageInfoModal()
  initializeModalKeyboardShortcuts()
}

/**
 * Initialize tag filter buttons
 */
function initializeTagFilters() {
  document.querySelectorAll('.btn-outline-primary').forEach(button => {
    button.addEventListener('click', function () {
      this.classList.toggle('active')
    })
  })
}

/**
 * Initialize search functionality
 */
function initializeSearchFunctionality() {
  const searchFields = document.querySelectorAll('.search-field')
  const filterForm = document.getElementById('filterForm')

  if (searchFields.length > 0 && filterForm) {
    let searchTimeout

    // Synchronize all search fields
    searchFields.forEach(field => {
      field.addEventListener('input', function (e) {
        const value = e.target.value

        // Update other visible fields to stay in sync
        searchFields.forEach(otherField => {
          if (otherField !== e.target) {
            otherField.value = value
          }
        })

        // Clear existing timeout
        clearTimeout(searchTimeout)

        // Set new timeout for auto-submit after 500ms
        searchTimeout = setTimeout(function () {
          filterForm.submit()
        }, 500)
      })

      // Handle Enter key to submit form immediately
      field.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault()
          // Clear the timeout since we're submitting immediately
          clearTimeout(searchTimeout)
          filterForm.submit()
        }
      })
    })
  }
}

/**
 * Perform search operation
 * @param {string} query - Search query
 */
function performSearch(query) {
  console.log('Performing search for:', query)

  // Update URL with search parameter
  const url = new URL(window.location)
  if (query.trim()) {
    url.searchParams.set('q', query)
  } else {
    url.searchParams.delete('q')
  }
  window.location.href = url.toString()
}

/**
 * Check if text element is being truncated
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - True if text is truncated
 */
function isTextTruncated(element) {
  const computedStyle = window.getComputedStyle(element)
  const lineHeight = parseFloat(computedStyle.lineHeight) || (parseFloat(computedStyle.fontSize) * 1.4)
  const maxHeight = lineHeight * 6
  return element.scrollHeight > maxHeight
}

/**
 * Initialize expand button visibility based on text truncation
 */
function initializeExpandButtons() {
  setTimeout(() => {
    document.querySelectorAll('.expand-btn').forEach(button => {
      const cardText = button.closest('.card-body').querySelector('.card-text')
      if (cardText && !isTextTruncated(cardText)) {
        button.style.display = 'none'
      }
    })
  }, 100)
}

/**
 * Toggle text expansion for card content
 * @param {HTMLElement} button - The expand/collapse button
 */
function toggleExpand(button) {
  const cardText = button.closest('.card-body').querySelector('.card-text')

  if (!cardText) {
    console.warn('Card text element not found')
    return
  }

  const isExpanded = cardText.classList.contains('text-expanded')

  if (isExpanded) {
    cardText.classList.remove('text-expanded')
    button.innerHTML = '<i class="bi bi-chevron-down me-1"></i>Show more'
  } else {
    cardText.classList.add('text-expanded')
    button.innerHTML = '<i class="bi bi-chevron-up me-1"></i>Show less'
  }
}

/**
 * Handle sort dropdown changes
 */
function initializeSortFunctionality() {
  const sortSelects = document.querySelectorAll('.ordering-field')
  const filterForm = document.getElementById('sidebarFilterForm')

  if (sortSelects.length > 0 && filterForm) {
    sortSelects.forEach(select => {
      select.addEventListener('change', function () {
        const sortValue = this.value
        console.log('Sort changed to:', sortValue)

        // Update other visible selects to stay in sync
        sortSelects.forEach(otherSelect => {
          if (otherSelect !== this) {
            otherSelect.value = sortValue
          }
        })

        // Submit the filter form
        filterForm.submit()
      })
    })
  }
}

/**
 * Handle filter form changes
 */
function initializeFilterFunctionality() {
  const filterElements = document.querySelectorAll('.sidebar-sticky input, .sidebar-sticky select, .offcanvas-body input, .offcanvas-body select')

  filterElements.forEach(element => {
    element.addEventListener('change', function () {
      console.log('Filter changed:', this.name || this.id, this.value || this.checked)
      // TODO: Implement auto-filtering or form submission
    })
  })
}

/**
 * Clear all filters
 */
function clearAllFilters() {
  // Clear checkboxes
  document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.checked = false
  })

  // Clear date inputs
  document.querySelectorAll('input[type="date"]').forEach(dateInput => {
    dateInput.value = ''
  })

  // Reset select elements
  document.querySelectorAll('select').forEach(select => {
    select.selectedIndex = 0
  })

  // Clear active tag buttons
  document.querySelectorAll('.btn-outline-primary.active').forEach(button => {
    button.classList.remove('active')
  })

  console.log('All filters cleared')
  // Reload page without filter parameters
  const url = new URL(window.location)
  url.search = ''
  window.location.href = url.toString()
}

/**
 * Initialize page info modal functionality
 */
function initializePageInfoModal() {
  const modal = document.getElementById('pageInfoModal')

  if (modal) {
    // Add event listeners for modal events
    modal.addEventListener('show.bs.modal', function () {
      console.log('Page info modal opening')
    })

    modal.addEventListener('shown.bs.modal', function () {
      // Focus the close button when modal is fully shown for accessibility
      const closeBtn = modal.querySelector('.modal-footer .btn')
      if (closeBtn) {
        closeBtn.focus()
      }
    })

    modal.addEventListener('hidden.bs.modal', function () {
      // Return focus to the info button when modal is closed
      const infoBtn = document.querySelector('.page-info-btn')
      if (infoBtn) {
        infoBtn.focus()
      }
    })
  }
}

/**
 * Handle keyboard shortcuts for modal
 */
function initializeModalKeyboardShortcuts() {
  document.addEventListener('keydown', function (event) {
    // Open modal with Ctrl/Cmd + I
    if ((event.ctrlKey || event.metaKey) && event.key === 'i') {
      event.preventDefault()
      const infoBtn = document.querySelector('.page-info-btn')
      if (infoBtn) {
        infoBtn.click()
      }
    }
  })
}

// Make functions globally available for onclick handlers
window.toggleExpand = toggleExpand
window.clearAllFilters = clearAllFilters
