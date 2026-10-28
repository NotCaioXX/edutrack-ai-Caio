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
- **Rationale**: Eliminates insecure direct object reference (IDOR) vulnerabilities, keeping user academic data strictly confidential.

### 3. XanoScript Query Primitives
- **Decision**: Use `db.query` for user-scoped lists, `db.get` for primary key lookup, `db.add` for inserts, `db.edit` for partial updates, and `db.del` for record deletion.
- **Rationale**: Direct adherence to standard XanoScript database manipulation semantics.

## Risks / Trade-offs

- **[Risk] IDOR or cross-tenant data leak** → Strict `precondition ($existing.user_id == $auth.id)` checks applied to any single-record fetch or mutation.
- **[Risk] Foreign key violation on task creation** → Precondition verifying that the referenced `subject_id` exists and belongs to the authenticated user before creating an academic task.

