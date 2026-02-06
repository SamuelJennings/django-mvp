# Feature Specification: Form View Mixin for Consistent Form Layouts (FormView, CreateView, UpdateView)

**Feature Branch**: `009-form-view-mixin`
**Created**: February 6, 2026
**Status**: Draft
**Input**: User description: "Create an MVPFormViewMixin (similar to MVPListViewMixin) that can be used with django basic forms views (FormView, CreateView, UpdateView) in order to create MVPFormView, MVPCreateView, and MVPUpdateView. We will need a view for each variant to demonstrate capabilities. The main functionality of the mixin will be to direct the view to a standard template that uses components from this package in order to create a consistent layout across all form views. The mixin should also attempt to detect which, if any, of the popular 3rd party form building packages are installed by the user. For instance, if django-crispy-forms is installed, then the template will render using the crispy_forms_tags templatetag library. If django-formset package is used, render_formset will be used in the template. Otherwise, render using form.as_p. DeleteView is explicitly out of scope for this feature."

## Clarifications

### Session 2026-02-06

- Q: When both django-crispy-forms and django-formset are installed, which rendering library should take precedence in the default priority order? → A: django-crispy-forms takes precedence (more widely adopted, mature, better Django ecosystem integration)
- Q: What specific form components should be included in the AdminLTE form layout template? → A: Card component with header (form title), body (form fields), and footer (submit/cancel buttons) initially, with potential for multiple template options in future iterations
- Q: Should form validation error messages be displayed at the top of the form, inline with each field, or both? → A: Both summary at top and inline per field for best accessibility and user experience
- Q: What should happen when a developer specifies a renderer that is not installed or properly configured? → A: Log warning and fall back to standard Django rendering (graceful degradation with developer visibility)
- Q: Should the mixin support inline formsets in the initial implementation? → A: Out of scope initially, will be addressed in a future feature to keep this implementation focused
- Q: Which Django form CBVs should be supported in this feature? → A: FormView, CreateView, and UpdateView. DeleteView will be addressed in a future feature. MVP classes should be named MVPFormView, MVPCreateView, MVPUpdateView (not MVPModelFormView)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Form Rendering with Automatic Layout (Priority: P1)

A developer creates a form view using MVPFormView and the system automatically renders it within the AdminLTE layout using the best available rendering method (crispy-forms, django-formset, or standard Django rendering).

**Why this priority**: This is the core functionality - developers need a quick way to create forms with consistent layouts without manually building templates for each form. This delivers immediate value by reducing boilerplate code.

**Independent Test**: Can be fully tested by creating a simple contact form using MVPFormView with standard Django forms and verifying it renders correctly in the AdminLTE layout using form.as_p styling.

**Acceptance Scenarios**:

1. **Given** a developer creates a class-based view inheriting from MVPFormView with a basic Django Form class, **When** they access the form page, **Then** the form renders within the AdminLTE layout using the standard form.as_p rendering method
2. **Given** a project has django-crispy-forms installed, **When** a developer creates an MVPFormView, **Then** the form automatically renders using crispy-forms template tags without requiring explicit configuration
3. **Given** a project has django-formset installed, **When** a developer creates an MVPFormView, **Then** the form automatically renders using render_formset without requiring explicit configuration
4. **Given** both django-crispy-forms and django-formset are installed, **When** a developer creates an MVPFormView without specifying a renderer, **Then** the form renders using a predictable default priority order
5. **Given** both rendering libraries are installed, **When** a developer sets a class attribute to specify their preferred renderer, **Then** the form renders using the explicitly specified renderer regardless of auto-detection
6. **Given** a developer creates an MVPFormView, **When** the form is submitted successfully, **Then** the success behavior follows standard Django form processing (redirect to success_url or display success message)

---

### User Story 2 - Model Form Create Support (Priority: P2)

A developer creates a model form view using MVPCreateView to create new database records with automatic layout and form rendering.

**Why this priority**: Create operations are fundamental to admin interfaces. This extends the base functionality to support model-based forms for creating new records, which is one of the most common use cases in Django applications.

**Independent Test**: Can be fully tested by creating an MVPCreateView for a simple model (e.g., Product with name and price fields) and verifying the create operation works correctly with the AdminLTE layout.

**Acceptance Scenarios**:

1. **Given** a developer creates an MVPCreateView for a model, **When** they access the create form page, **Then** a new model form renders within the AdminLTE layout
2. **Given** a user submits a valid model form, **When** processing completes, **Then** the record is saved to the database and the user is redirected appropriately
3. **Given** a user submits an invalid model form, **When** validation fails, **Then** the form redisplays with error messages and previously entered data preserved

---

### User Story 3 - Model Form Edit Support (Priority: P2)

A developer creates a model form view using MVPUpdateView to edit existing database records with automatic layout and form rendering.

**Why this priority**: Update operations complete the core CRUD functionality. This enables developers to provide full record management capabilities with consistent AdminLTE layouts.

**Independent Test**: Can be fully tested by creating an MVPUpdateView for a simple model (e.g., Product) and verifying the edit operation pre-populates data, validates changes, and saves updates correctly with the AdminLTE layout.

**Acceptance Scenarios**:

1. **Given** a developer creates an MVPUpdateView for a model, **When** they access an edit form with an instance pk, **Then** the form is pre-populated with the existing model instance data
2. **Given** a user submits valid changes to an update form, **When** processing completes, **Then** the record is updated in the database and the user is redirected appropriately
3. **Given** a user submits invalid changes to an update form, **When** validation fails, **Then** the form redisplays with error messages and the user's attempted changes preserved

---

### User Story 4 - Demonstration Views (Priority: P3)

A developer exploring the package can view working examples of form views that demonstrate all supported rendering methods and configurations.

**Why this priority**: Good examples accelerate adoption and reduce confusion. While not core functionality, demonstration views help developers understand capabilities and best practices.

**Independent Test**: Can be fully tested by navigating to the demo section and verifying example forms render correctly using each supported method (basic Django, crispy-forms, django-formset), without needing to write any code.

**Acceptance Scenarios**:

1. **Given** the demo application is running, **When** a developer navigates to the form demos section, **Then** they see working examples of MVPFormView, MVPCreateView, and MVPUpdateView
2. **Given** multiple form rendering libraries are available, **When** viewing the demos, **Then** each rendering method is demonstrated with clear labels indicating which library is being used
3. **Given** a developer views form demo source code, **When** they examine the view implementation, **Then** they see minimal boilerplate code demonstrating how easy it is to use the mixins

---

### Edge Cases

- What happens when both crispy-forms and django-formset are installed simultaneously? **Clarified:** Crispy-forms takes precedence by default
- What happens when a developer explicitly specifies a renderer that is not installed or properly configured? **Clarified:** System logs warning and falls back to standard Django rendering
- How does the system handle custom form widgets that may conflict with auto-detected rendering methods?
- What happens if a form rendering library is installed but not properly configured in Django settings? **Clarified:** Falls back to standard Django rendering with warning logged
- What happens when a form has no fields (edge case in dynamic form generation)?
- **Out of scope:** Inline formsets are not supported in this feature and will be addressed in future work
- **Out of scope:** DeleteView is not supported in this feature and will be addressed in future work

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an MVPFormViewMixin that can be composed with Django's FormView to create consistent form layouts
- **FR-002**: System MUST provide an MVPFormView class that combines MVPFormViewMixin with Django's FormView
- **FR-003**: System MUST provide an MVPCreateView class that combines MVPFormViewMixin with Django's CreateView
- **FR-004**: System MUST provide an MVPUpdateView class that combines MVPFormViewMixin with Django's UpdateView
- **FR-005**: System MUST automatically detect which form rendering libraries are installed (django-crispy-forms, django-formset)
- **FR-006**: System MUST use crispy-forms rendering when django-crispy-forms is detected and properly configured
- **FR-007**: System MUST use django-formset rendering when django-formset is detected and properly configured
- **FR-008**: System MUST fall back to Django's standard form.as_p rendering when no third-party rendering library is available
- **FR-009**: System MUST provide a default template that uses AdminLTE layout components for consistent form presentation
- **FR-010**: System MUST allow developers to override the auto-detection behavior by setting a class attribute that specifies their preferred rendering method
- **FR-011**: System MUST follow a predictable priority order when multiple rendering libraries are installed and no explicit renderer is specified (priority: crispy-forms > django-formset > standard Django)
- **FR-012**: System MUST log a warning and fall back to standard Django rendering when an explicitly specified renderer is not installed or properly configured
- **FR-013**: System MUST maintain all standard Django form view behaviors (form_valid, form_invalid, get_success_url, etc.)
- **FR-014**: System MUST provide demonstration views showing MVPFormView usage with basic forms
- **FR-015**: System MUST provide demonstration views showing MVPCreateView usage for creating model records
- **FR-016**: System MUST provide demonstration views showing MVPUpdateView usage for editing model records
- **FR-017**: System MUST provide demonstration views showing explicit renderer specification when multiple libraries are available
- **FR-018**: System MUST display form validation errors both as a summary at the top of the form and inline with each field that has errors
- **FR-019**: System MUST use AdminLTE card component structure (header, body, footer) for form layout presentation
- **FR-020**: System MUST support standard Django form success patterns (redirect on success, display messages)
- **FR-021**: System MUST preserve form field data when validation fails and the form is redisplayed
- **FR-022**: Inline formsets are explicitly out of scope for this feature
- **FR-023**: DeleteView is explicitly out of scope for this feature and will be addressed in future work

### Key Entities *(include if feature involves data)*

- **FormView Configuration**: Settings that control form rendering behavior including auto-detection preferences, template selection, and rendering method overrides
- **Form Rendering Method**: The approach used to render forms with priority order: crispy-forms (highest) > django-formset > standard Django (fallback)
- **Form Layout Structure**: AdminLTE card-based layout with header (title), body (form fields with inline errors), and footer (action buttons)
- **Error Display System**: Dual error presentation showing both summary at top and inline field-level errors
- **Demo Form**: Example form used in demonstration views showing basic form fields and validation
- **Demo Model**: Example database model used in demonstration views showing model form creation and editing

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can create a working form view with AdminLTE layout in under 10 lines of code (class definition with form_class and success_url)
- **SC-002**: Form rendering automatically adapts based on installed libraries without requiring developer configuration in 100% of standard cases
- **SC-003**: All demonstration views render successfully and display forms using the appropriate rendering method based on installed dependencies
- **SC-004**: Form validation errors display clearly within the AdminLTE layout and allow users to correct mistakes without losing entered data
- **SC-005**: The mixin integrates seamlessly with existing Django CBV patterns without requiring developers to learn new concepts beyond standard Django form views
