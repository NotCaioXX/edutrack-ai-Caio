# Design

## Context

EduTrack AI features a Streamlit application (`app.py`) as the user interface and a Xano backend architecture (`tables/`, `apis/`, `functions/`). The current application contains placeholder sections for "Disciplinas" and dashboard metrics ("Disciplinas Ativas: 0"), while the backend has user and account tables but no schema or endpoints for academic courses.

See `proposal.md` for background and motivation, and `specs/subjects/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Define the Xano data schema for academic subjects (`subject` table) associated with the student user.
- Define RESTful API endpoints for subject operations: list subjects, create subject, retrieve subject, update subject, delete subject.
- Update the Streamlit frontend (`app.py`) to provide an interactive interface to list, create, and view subjects, and wire up the active subjects count metric on the dashboard.

**Non-Goals:**
- Grade calculations, attendance logs, and syllabus document uploads (reserved for subsequent iterations).
- Class scheduling / calendar integrations.

## Decisions

### 1. Dedicated `subjects` Table with User Association
- **Decision**: Create a dedicated table (`subjects`) with fields:
  - `id` (int, autoincrement, primary key)
  - `created_at` (timestamp, default now)
  - `user_id` (int, foreign key referencing `user`)
  - `name` (text, required, filter: trim)
  - `teacher` (text, optional, filter: trim)
  - `hours` (int, optional, filter: min:0)
- **Indexes**:
  - Primary key on `id`
  - B-tree index on `user_id` (foreign key for user scoping)
- **Alternatives Considered**: Storing subjects as a JSON array field inside the `user` table.
- **Rationale**: Relational table adheres to Xano best practices, ensures data integrity, and enables foreign key linkage to upcoming task/assignment entities.

### 2. Standardized REST Endpoints in Xano
- **Decision**: Expose endpoints under a `subjects` API group:
  - `GET /subjects` (list subjects for current user, filterable by status)
  - `POST /subjects` (create subject)
  - `GET /subjects/{id}` (fetch details)
  - `PATCH /subjects/{id}` (update subject)
  - `DELETE /subjects/{id}` (delete subject)
- **Alternatives Considered**: GraphQL or single RPC function.
- **Rationale**: Standard REST endpoints map cleanly to Xano conventions and Streamlit HTTP client integrations.

### 3. Frontend Architecture in Streamlit
- **Decision**: Build an intuitive UI in `app.py` under the "Disciplinas" menu with tabs or sections for viewing current subjects and a form for adding a new subject. Provide resilient backend connectivity handling with user feedback.
- **Alternatives Considered**: Separate multi-page Streamlit app.
- **Rationale**: Preserves the single-app structure while keeping navigation straightforward for students.

### 4. Delegation Strategy
- **Decision**: In alignment with `AGENTS.md`, implementation of XanoScript tables and API queries will be staged and delegated to specialized agents (Xano Table Designer and Xano API Query Writer).

## Risks / Trade-offs

- **[Risk] Multi-tenant data exposure**: A user could access or modify another student's subjects.
  - **Mitigation**: All backend queries enforce user authentication filters ensuring operations are scoped to `auth.id` / `user_id`.
- **[Risk] Backend connectivity during local development**: Streamlit app may fail if Xano endpoints are temporarily offline or unconfigured.
  - **Mitigation**: Add error handling in frontend with informational alerts and guidance on configuring backend connection parameters.

## Migration Plan

1. Implement and deploy the `subject` table schema to Xano.
2. Implement and test the `/subjects` API group endpoints.
3. Update `app.py` in the frontend to connect with the backend and display real-time subject data and metrics.
