# Design

## Context

EduTrack AI's database models for academic entities (`subjects` and `academic_tasks`) are defined in XanoScript (`tables/subjects.xs` and `tables/academic_tasks.xs`). Both entities include an `int user_id` foreign key referencing the `user` table. To support secure client operations, backend endpoints must be exposed under organized API groups with strict multi-tenant authorization guards.

## Goals / Non-Goals

**Goals:**
- Provide full RESTful CRUD operations (`POST`, `GET`, `PATCH`, `DELETE`) for the `subjects` table.
- Provide full RESTful CRUD operations (`POST`, `GET`, `PATCH`, `DELETE`) for the `academic_tasks` table.
- Enforce that all reads and mutations are scoped to `$auth.id` using `auth = "user"`.
- Validate required inputs (e.g., subject name, task title, subject foreign key).

**Non-Goals:**
- Frontend modifications (Streamlit interfaces already consume these endpoint contracts).
- Administrative cross-user endpoints or bulk data import workflows.

## Decisions

### 1. API Group Organization
- **Decision**: Organize endpoints into modular API groups:
  - `api/subjects/`: Contains group definition and subject CRUD endpoints.
  - `api/academic_tasks/`: Contains group definition and academic task CRUD endpoints.
- **Rationale**: Follows XanoScript modular project structure, aligning with existing API groups (`api/authentication/`, `api/event_logs/`).

### 2. Multi-Tenant Ownership Verification
- **Decision**: 
  - For list queries (`GET /subjects`, `GET /academic_tasks`): filter by `$db.user_id == $auth.id`.
  - For creation (`POST`): automatically assign `user_id: $auth.id` from the decoded authentication token rather than accepting arbitrary user IDs from the client payload.
  - For mutations by ID (`GET /{id}`, `PATCH /{id}`, `DELETE /{id}`):
    ```xs
    precondition ($existing_record.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
    ```
- **Rationale**: Eliminates insecure direct object references (IDOR) and guarantees complete isolation between students.

### 3. Database Operation Syntax
- **Decision**: Use `db.query` for lists, `db.get` for single records, `db.add` for insertion, `db.edit` for updates, and `db.del` for deletions.
- **Rationale**: Strictly conforms to the XanoScript language server grammar and built-in database functions.

## Risks / Trade-offs

- **[Risk] IDOR Vulnerability**: A student attempting to inspect or alter another student's task by altering the route parameter `{id}`.
  - **Mitigation**: Precondition asserts `$record.user_id == $auth.id` before any data is returned, updated, or removed.
- **[Risk] Unlinked task references**: Task created referencing a subject belonging to another user.
  - **Mitigation**: In `POST /academic_tasks`, verify that `subject_id` points to a subject owned by `$auth.id`.

## Migration Plan

1. Structure API files in `api/subjects/` and `api/academic_tasks/`.
2. Validate syntax using the XanoScript language server parser.

