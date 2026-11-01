# Proposal

## Why

EduTrack AI requires comprehensive RESTful CRUD operations for managing both academic subjects (`subjects`) and tasks (`academic_tasks`). In a multi-tenant academic platform, data isolation and privacy are paramount: each student must only be permitted to access, modify, and delete records belonging to their authenticated account. Providing standardized, secure CRUD endpoints with strict ownership verification prevents unauthorized data leakage and establishes a reliable API contract for frontend integration.

## What Changes

- Implement complete authenticated CRUD endpoints for `subjects`:
  - `GET /subjects`: List all subjects belonging to the authenticated user.
  - `GET /subjects/{subjects_id}`: Retrieve a specific subject belonging to the user.
  - `POST /subjects`: Create a new subject assigned to `$auth.id`.
  - `PATCH /subjects/{subjects_id}`: Update subject fields with ownership validation.
  - `DELETE /subjects/{subjects_id}`: Remove a subject with ownership validation.
- Implement complete authenticated CRUD endpoints for `academic_tasks`:
  - `GET /academic_tasks`: List all tasks belonging to the authenticated user.
  - `GET /academic_tasks/{academic_tasks_id}`: Retrieve a specific task belonging to the user.
  - `POST /academic_tasks`: Create a new task assigned to `$auth.id` linked to a subject.
  - `PATCH /academic_tasks/{academic_tasks_id}`: Update task fields (status, deadline, description) with ownership validation.
  - `DELETE /academic_tasks/{academic_tasks_id}`: Remove a task with ownership validation.
- Enforce strict ownership policies across all queries using `auth = "user"` and verifying `user_id == $auth.id`.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `academic-crud`: Refine and reinforce secure CRUD operations and data ownership constraints for subjects and academic tasks.

## Impact

- **Backend / APIs**: Creation of structured API definitions under `api/subjects/` and `api/academic_tasks/`.
- **Database**: Relies on `tables/subjects.xs` and `tables/academic_tasks.xs` schemas and indices.
- **Security**: All endpoints enforce `auth = "user"`, denying access to unauthenticated requests and requests targeting records belonging to another student.

