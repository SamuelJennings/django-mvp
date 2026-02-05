document.addEventListener('DOMContentLoaded', function () {
  const toggles = document.querySelectorAll('[data-mvp-toggle]')
  toggles.forEach(toggle => {
    toggle.addEventListener('click', function () {
      const toggleValue = this.getAttribute('data-mvp-toggle')
      let targetClass
      switch (toggleValue) {
        case 'sidebar-left': targetClass = 'mvp-sidebar-left'; break
        case 'header': targetClass = 'mvp-header'; break
        case 'footer': targetClass = 'mvp-footer'; break
        case 'sidebar-right': targetClass = 'mvp-sidebar-right'; break
        default: return
      }
      let layout
      const layoutSelector = this.getAttribute('data-mvp-layout')
      if (layoutSelector) {
        layout = document.querySelector(layoutSelector)
      } else {
        layout = this.closest('.mvp-layout')
      }
      if (!layout) return
      const target = layout.querySelector(':scope > .' + targetClass)
      if (!target) return
      const isHorizontal = target.classList.contains('collapse-horizontal')
      const dimension = isHorizontal ? 'width' : 'height'
      const isShown = target.classList.contains('show')
      if (isShown) {
        // hide
        const size = isHorizontal ? target.offsetWidth : target.offsetHeight
        target.style[dimension] = size + 'px'
        target.offsetWidth // force reflow
        target.classList.remove('collapse', 'show')
        target.classList.add('collapsing')
        target.style[dimension] = '0px'
        target.addEventListener('transitionend', function handler(e) {
          if (e.target !== target) return
          target.removeEventListener('transitionend', handler)
          target.classList.remove('collapsing')
          target.classList.add('collapse')
          target.style[dimension] = ''
          target.style.transition = ''
        })
      } else {
        // show
        target.classList.remove('collapse')
        target.classList.add('collapsing')
        target.style[dimension] = '0px'
        target.offsetWidth // force reflow
        const size = isHorizontal ? target.scrollWidth : target.scrollHeight
        target.style[dimension] = size + 'px'
        target.addEventListener('transitionend', function handler(e) {
          if (e.target !== target) return
          target.removeEventListener('transitionend', handler)
          target.classList.remove('collapsing')
          target.classList.add('show', 'collapse')
          target.style[dimension] = ''
          target.style.transition = ''
        })
      }
    })
  })
})
