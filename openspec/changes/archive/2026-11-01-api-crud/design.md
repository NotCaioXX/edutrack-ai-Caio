# Design

## Context

EduTrack AI features a Streamlit frontend and a Xano backend. Tables `subjects` and `academic_tasks` are already defined in `table/subjects.xs` and `table/academic_tasks.xs`. Endpoints must guarantee strict multi-tenant isolation by enforcing that only records belonging to `$auth.id` can be read, written, updated, or removed. The Streamlit pages `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` interact with these endpoints, requiring authenticated HTTP requests using the session Bearer token.

See `proposal.md` for motivation and `specs/academic-crud/spec.md` for detailed behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Provide complete RESTful CRUD endpoints (`GET`, `POST`, `PATCH`, `DELETE`) in XanoScript for `subjects` and `academic_tasks`.
- Enforce strict ownership validation (`user_id == $auth.id`) across all endpoints.
- Ensure the Streamlit frontend (`Disciplinas` and `Tarefas` pages) performs live queries and persistent storage directly with Xano using authenticated requests.

**Non-Goals:**
- Automatic execution of deployment or push tools (`push_all_changes_to_xano`), adhering to Rule #2 in `AGENTS.md`.
- Unrequested functionality such as grade reporting, CSV exports, or bulk batch operations.

## Decisions

### 1. Ownership Filtering in XanoScript Queries
- **Decision**: In all listing endpoints (`GET /subjects`, `GET /academic_tasks`), apply `where = $db.user_id == $auth.id`.
- **Decision**: In creation endpoints (`POST`), assign `user_id: $auth.id` from the auth context rather than taking `user_id` from unverified user input. In `POST /academic_tasks`, verify that the referenced `subject_id` belongs to the authenticated user.
- **Decision**: In single-record operations (`GET /:id`, `PATCH /:id`, `DELETE /:id`), include a precondition verifying that the record exists and `record.user_id == $auth.id`.
- **Rationale**: Prevents IDOR (Insecure Direct Object Reference) vulnerabilities and ensures complete multi-tenant safety.

### 2. Frontend Session Token Integration
- **Decision**: Streamlit pages obtain the JWT token from `st.session_state["auth_token"]` and supply it via `Authorization: Bearer <token>` headers in all calls to `BASE_URL`.
- **Decision**: When `BASE_URL` or `auth_token` is unavailable, display a user-friendly guidance message directing the user to login on the Perfil page.
- **Rationale**: Maintains a smooth user experience while ensuring backend requests are properly authenticated.

## Risks / Trade-offs

- **[Risk] Unauthenticated user attempt**: User opens Disciplinas or Tarefas without logging in on Perfil page.
  - **Mitigation**: Frontend informs user via status banner and disables form submission or prompts for login.
- **[Risk] Network connectivity issues**: API requests timeout or fail.
  - **Mitigation**: Catch `requests.exceptions.RequestException`, display appropriate error feedback, and avoid crashing the Streamlit app.

## Migration Plan

1. Verify and ensure all XanoScript CRUD endpoints exist under `api/subjects/` and `api/academic_tasks/`.
2. Update and verify `pages/1_📚_Disciplinas.py` to ensure all CRUD actions save to and load from Xano.
3. Update and verify `pages/2_📝_Tarefas.py` to ensure all CRUD actions save to and load from Xano.

