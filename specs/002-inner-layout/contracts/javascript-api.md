# JavaScript API Contract

**Feature**: 002-inner-layout  
**Version**: 1.0.0  
**Date**: 2025-12-23

## Contract Overview

This document defines the stable JavaScript API for inner layout behavior (collapse and offcanvas state management). This API is part of the public contract and breaking changes require a MAJOR version bump.

## Architecture

**Language**: TypeScript (compiled to JavaScript)  
**Output**: ES5/ES6 bundle at `mvp/static/js/inner_layout.js`  
**Dependencies**: Bootstrap 5.3+ (for offcanvas functionality)  
**Pattern**: Progressive enhancement (layout works without JavaScript)

## Public API

### InnerLayoutManager Class

Main class for managing inner layout state.

#### Constructor

```typescript
constructor(options?: InnerLayoutOptions)
```

**Parameters**:
```typescript
interface InnerLayoutOptions {
  // Primary sidebar selector
  primarySelector?: string;      // Default: '#primarySidebar'
  
  // Secondary sidebar selector
  secondarySelector?: string;    // Default: '#secondarySidebar'
  
  // Breakpoint for offcanvas mode (px)
  breakpoint?: number;           // Default: 768 (md)
  
  // Enable localStorage persistence
  persistState?: boolean;        // Default: true
  
  // Debug logging
  debug?: boolean;               // Default: false
}
```

**Example**:
```javascript
const layout = new InnerLayoutManager({
  primarySelector: '#mySidebar',
  breakpoint: 992,  // lg breakpoint
  debug: true
});
```

---

#### Methods

##### `init(): void`

Initialize the layout manager, set up event listeners, restore persisted state.

**Behavior**:
- Finds sidebar elements via selectors
- Attaches click handlers to collapse toggle buttons
- Restores collapsed state from localStorage
- Sets up resize listener for breakpoint detection
- Initializes Bootstrap offcanvas instances

**Example**:
```javascript
const layout = new InnerLayoutManager();
layout.init();
```

**Contract**: MUST be called before any other methods. Safe to call multiple times (idempotent).

---

##### `toggleCollapse(sidebar: 'primary' | 'secondary'): boolean`

Toggle collapse state for specified sidebar.

**Parameters**:
- `sidebar`: Which sidebar to toggle (`'primary'` or `'secondary'`)

**Returns**: 
- `true` if toggle succeeded
- `false` if toggle blocked (e.g., in offcanvas mode)

**Behavior**:
- Checks if in offcanvas mode (viewport < breakpoint)
- If offcanvas mode: logs warning, returns false
- If normal mode: toggles `.collapsed` class, saves to localStorage, returns true

**Example**:
```javascript
const layout = new InnerLayoutManager();
layout.init();

// Toggle primary sidebar
if (!layout.toggleCollapse('primary')) {
  console.log('Cannot collapse in offcanvas mode');
}
```

**Contract**: MUST NOT collapse sidebar when viewport < breakpoint.

---

##### `isCollapsed(sidebar: 'primary' | 'secondary'): boolean`

Check if sidebar is currently collapsed.

**Parameters**:
- `sidebar`: Which sidebar to check

**Returns**: `true` if collapsed, `false` otherwise

**Example**:
```javascript
if (layout.isCollapsed('primary')) {
  console.log('Primary sidebar is collapsed');
}
```

---

##### `isOffcanvasMode(): boolean`

Check if layout is currently in offcanvas mode (viewport < breakpoint).

**Returns**: `true` if offcanvas mode active, `false` otherwise

**Example**:
```javascript
if (layout.isOffcanvasMode()) {
  console.log('Mobile view - sidebars are offcanvas');
}
```

**Contract**: MUST return true when `window.innerWidth < breakpoint`.

---

##### `expandSidebar(sidebar: 'primary' | 'secondary'): void`

Programmatically expand a collapsed sidebar.

**Parameters**:
- `sidebar`: Which sidebar to expand

**Behavior**:
- Removes `.collapsed` class
- Updates localStorage
- Does nothing if sidebar already expanded

**Example**:
```javascript
layout.expandSidebar('primary');
```

---

##### `collapseSidebar(sidebar: 'primary' | 'secondary'): boolean`

Programmatically collapse a sidebar.

**Parameters**:
- `sidebar`: Which sidebar to collapse

**Returns**:
- `true` if collapse succeeded
- `false` if blocked (offcanvas mode)

**Behavior**:
- Checks offcanvas mode constraint
- Adds `.collapsed` class if allowed
- Updates localStorage

**Example**:
```javascript
if (!layout.collapseSidebar('secondary')) {
  console.log('Cannot collapse - viewport too small');
}
```

**Contract**: MUST NOT allow collapse when in offcanvas mode.

---

##### `destroy(): void`

Clean up event listeners and state.

**Behavior**:
- Removes all event listeners
- Clears localStorage (if persistState was true)
- Nulls out references

**Example**:
```javascript
const layout = new InnerLayoutManager();
layout.init();

// Later, when cleaning up
layout.destroy();
```

**Contract**: After calling, instance should not be used. Create new instance if needed.

---

## Events

The manager dispatches custom events for integration with other code.

### Event: `innerlayout:collapsed`

Fired when a sidebar is collapsed.

**Event Detail**:
```typescript
interface CollapseEventDetail {
  sidebar: 'primary' | 'secondary';
  timestamp: number;
}
```

**Example**:
```javascript
document.addEventListener('innerlayout:collapsed', (event) => {
  console.log(`${event.detail.sidebar} sidebar collapsed`);
});
```

---

### Event: `innerlayout:expanded`

Fired when a sidebar is expanded.

**Event Detail**:
```typescript
interface ExpandEventDetail {
  sidebar: 'primary' | 'secondary';
  timestamp: number;
}
```

**Example**:
```javascript
document.addEventListener('innerlayout:expanded', (event) => {
  console.log(`${event.detail.sidebar} sidebar expanded`);
});
```

---

### Event: `innerlayout:offcanvasmode`

Fired when layout enters offcanvas mode (viewport shrinks below breakpoint).

**Event Detail**:
```typescript
interface OffcanvasModeEventDetail {
  active: boolean;  // true when entering, false when exiting
  breakpoint: number;
  viewport: number;
}
```

**Example**:
```javascript
document.addEventListener('innerlayout:offcanvasmode', (event) => {
  if (event.detail.active) {
    console.log('Entered offcanvas mode');
  } else {
    console.log('Exited offcanvas mode');
  }
});
```

---

## Bootstrap Offcanvas Integration

The component integrates with Bootstrap's offcanvas JavaScript API.

### Offcanvas Events

Bootstrap fires events on offcanvas elements:

```javascript
const primarySidebar = document.getElementById('primarySidebar');

// Before opening
primarySidebar.addEventListener('show.bs.offcanvas', () => {
  console.log('Opening primary sidebar');
});

// After opening (with transition complete)
primarySidebar.addEventListener('shown.bs.offcanvas', () => {
  console.log('Primary sidebar opened');
});

// Before closing
primarySidebar.addEventListener('hide.bs.offcanvas', () => {
  console.log('Closing primary sidebar');
});

// After closing
primarySidebar.addEventListener('hidden.bs.offcanvas', () => {
  console.log('Primary sidebar closed');
});
```

### Programmatic Offcanvas Control

```javascript
const primarySidebar = document.getElementById('primarySidebar');
const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(primarySidebar);

// Show offcanvas
offcanvas.show();

// Hide offcanvas
offcanvas.hide();

// Toggle offcanvas
offcanvas.toggle();
```

**Contract**: InnerLayoutManager MUST NOT interfere with Bootstrap's offcanvas management.

---

## Local Storage Schema

The manager persists sidebar collapse state to localStorage.

### Storage Keys

| Key | Type | Description |
|-----|------|-------------|
| `innerLayout.primarySidebar.collapsed` | `boolean` | Primary sidebar collapse state |
| `innerLayout.secondarySidebar.collapsed` | `boolean` | Secondary sidebar collapse state |

### Storage Contract

**Contract**:
- State MUST be saved on every collapse/expand action
- State MUST be restored on init()
- State MUST be cleared on destroy()
- State MUST NOT be persisted for offcanvas open/closed (Bootstrap handles)

**Example**:
```javascript
// Manual state check
const isCollapsed = localStorage.getItem('innerLayout.primarySidebar.collapsed') === 'true';

// Clear all inner layout state
localStorage.removeItem('innerLayout.primarySidebar.collapsed');
localStorage.removeItem('innerLayout.secondarySidebar.collapsed');
```

---

## Progressive Enhancement

**Contract**: Layout MUST work without JavaScript.

### No-JS Behavior

When JavaScript is disabled or fails to load:

1. **Sidebars**: Render in normal mode (not collapsed)
2. **Offcanvas**: Bootstrap CSS handles responsive behavior via `.offcanvas-md`
3. **Collapse**: Toggle buttons hidden/non-functional (gracefully degrade)
4. **Main Content**: Always accessible and scrollable

### JavaScript Enhancement

When JavaScript loads:

1. **Collapse Toggles**: Become functional
2. **State Persistence**: Sidebar collapse state restored from localStorage
3. **Constraint Enforcement**: Collapse disabled in offcanvas mode
4. **Events**: Custom events fired for integration

**Testing**:
```html
<!-- Test with JS disabled in DevTools -->
<c-layouts.inner>
  <c-slot name="primary_sidebar">Navigation</c-slot>
  <h1>Main Content</h1>
</c-layouts.inner>
<!-- Should still render and be navigable -->
```

---

## TypeScript Types

### Exported Types

```typescript
// Options for InnerLayoutManager
export interface InnerLayoutOptions {
  primarySelector?: string;
  secondarySelector?: string;
  breakpoint?: number;
  persistState?: boolean;
  debug?: boolean;
}

// Sidebar identifier
export type SidebarIdentifier = 'primary' | 'secondary';

// Event detail types
export interface CollapseEventDetail {
  sidebar: SidebarIdentifier;
  timestamp: number;
}

export interface ExpandEventDetail {
  sidebar: SidebarIdentifier;
  timestamp: number;
}

export interface OffcanvasModeEventDetail {
  active: boolean;
  breakpoint: number;
  viewport: number;
}
```

### Usage in TypeScript Projects

```typescript
import { InnerLayoutManager, InnerLayoutOptions } from './inner_layout';

const options: InnerLayoutOptions = {
  breakpoint: 992,
  debug: true
};

const layout = new InnerLayoutManager(options);
layout.init();
```

---

## Browser Compatibility

**Target**: ES5 compatibility for wide browser support

**Compiled Output**: Transpiled to ES5 via TypeScript compiler

**Minimum Browser Versions**:
- Chrome: 60+
- Firefox: 60+
- Safari: 12+
- Edge: 79+

**Polyfills Required**: None (component uses only widely-supported APIs)

**Contract**: Compiled JavaScript MUST work in all target browsers without polyfills.

---

## Error Handling

### Graceful Degradation

```typescript
class InnerLayoutManager {
  init(): void {
    try {
      // Find sidebars
      this.primarySidebar = document.querySelector(this.options.primarySelector);
      this.secondarySidebar = document.querySelector(this.options.secondarySelector);
      
      if (!this.primarySidebar && !this.secondarySidebar) {
        console.warn('InnerLayoutManager: No sidebars found');
        return;  // Exit gracefully
      }
      
      // Continue initialization
    } catch (error) {
      console.error('InnerLayoutManager init failed:', error);
      // Don't throw - allow page to function
    }
  }
}
```

**Contract**: Errors MUST NOT break page functionality. Log errors and degrade gracefully.

---

## Testing Contract

### Unit Tests

```typescript
describe('InnerLayoutManager', () => {
  test('toggleCollapse returns false in offcanvas mode', () => {
    // Mock viewport at 500px (< 768px breakpoint)
    global.innerWidth = 500;
    const layout = new InnerLayoutManager();
    layout.init();
    
    expect(layout.toggleCollapse('primary')).toBe(false);
  });
  
  test('toggleCollapse succeeds in normal mode', () => {
    // Mock viewport at 1024px (> 768px breakpoint)
    global.innerWidth = 1024;
    const layout = new InnerLayoutManager();
    layout.init();
    
    expect(layout.toggleCollapse('primary')).toBe(true);
  });
  
  test('state persisted to localStorage', () => {
    const layout = new InnerLayoutManager();
    layout.init();
    layout.collapseSidebar('primary');
    
    expect(localStorage.getItem('innerLayout.primarySidebar.collapsed')).toBe('true');
  });
});
```

---

## Versioning

Changes to this API follow Semantic Versioning:

**MAJOR** (Breaking):
- Removing public methods
- Changing method signatures
- Removing events
- Changing event detail structure
- Removing exported types
- Changing localStorage schema (keys/structure)

**MINOR** (Non-breaking):
- Adding new methods
- Adding new events
- Adding new exported types
- Adding new options to InnerLayoutOptions (with defaults)

**PATCH** (Bug fixes):
- Fixing constraint enforcement bugs
- Fixing state persistence issues
- Fixing browser compatibility
- Performance improvements

Current version: **1.0.0** (initial release)

---

## Migration from Existing Implementation

### Current Implementation

Existing `mvp/static/js/inner_layout.js` provides basic collapse functionality.

### Migration Path

**v1.0.0** (This specification):
- Maintain backwards compatibility with existing collapse toggles
- Add offcanvas constraint enforcement
- Add TypeScript source
- Add proper event system
- Keep same localStorage keys

**Breaking Changes**: None expected if existing code only uses:
- Collapse toggle buttons (`.inner-primary-toggle`, `.inner-secondary-toggle`)
- LocalStorage keys (`innerLayout.*.collapsed`)

**New Features** (Non-breaking):
- Programmatic API via InnerLayoutManager class
- Custom events for integration
- Offcanvas mode detection
- Improved constraint enforcement
