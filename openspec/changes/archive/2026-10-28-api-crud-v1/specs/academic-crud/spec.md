# Spec Delta

## Purpose

Provides secure, authenticated RESTful CRUD endpoints for subjects and academic tasks, enforcing strict multi-tenant user data isolation.

## ADDED Requirements

### Requirement: Secure Subject CRUD Operations
The system SHALL provide authenticated endpoints to create, list, retrieve, update, and delete subjects, ensuring each student only accesses and modifies their own subject records.

#### Scenario: User queries own subjects
- **WHEN** an authenticated student requests their subjects list via `GET /subjects`
- **THEN** the system returns only subjects where `user_id` matches the authenticated user

#### Scenario: User attempts to access another student's subject
- **WHEN** a user attempts to retrieve, modify, or delete a subject belonging to another user
- **THEN** the system rejects the request with an access denied or not found error

#### Scenario: Create subject with authenticated user association
- **WHEN** an authenticated user creates a subject via `POST /subjects`
- **THEN** the record is created with `user_id` mapped to the authenticated user ID

### Requirement: Secure Academic Task CRUD Operations
The system SHALL provide authenticated endpoints to create, list, retrieve, update, and delete academic tasks, ensuring each student only accesses and modifies their own tasks.

#### Scenario: User queries own academic tasks
- **WHEN** an authenticated student requests their tasks list via `GET /academic_tasks`
- **THEN** the system returns only tasks where `user_id` matches the authenticated user

#### Scenario: User attempts to modify another student's task
- **WHEN** a user attempts to update or delete a task belonging to a different user
- **THEN** the system rejects the operation with an access denied error

#### Scenario: Create task linked to subject and user
- **WHEN** an authenticated user creates a task via `POST /academic_tasks`
- **THEN** the system records the task with `user_id` mapped to the authenticated user and links it to the specified `subject_id`

