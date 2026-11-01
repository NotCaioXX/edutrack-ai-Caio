# Proposal

## Why

EduTrack AI requires comprehensive RESTful CRUD operations for managing both academic subjects (`subjects`) and tasks (`academic_tasks`). In an academic environment, multi-tenant data isolation and privacy are paramount: each student must only access, modify, and delete records belonging to their authenticated account. Furthermore, the Streamlit frontend pages for Disciplinas and Tarefas must actively synchronize with Xano, saving new entries to the backend and retrieving updated data directly from it.

## What Changes

- Implement and verify complete authenticated CRUD endpoints for `subjects` in XanoScript:
  - `GET /subjects`: List all subjects belonging to the authenticated user (`user_id == $auth.id`).
  - `GET /subjects/{subjects_id}`: Retrieve a specific subject belonging to the authenticated user.
  - `POST /subjects`: Create a new subject assigned to `$auth.id`.
  - `PATCH /subjects/{subjects_id}`: Update subject fields with ownership validation.
  - `DELETE /subjects/{subjects_id}`: Remove a subject with ownership validation.
- Implement and verify complete authenticated CRUD endpoints for `academic_tasks` in XanoScript:
  - `GET /academic_tasks`: List all tasks belonging to the authenticated user (`user_id == $auth.id`).
  - `GET /academic_tasks/{academic_tasks_id}`: Retrieve a specific task belonging to the authenticated user.
  - `POST /academic_tasks`: Create a new task assigned to `$auth.id` linked to a valid user subject.
  - `PATCH /academic_tasks/{academic_tasks_id}`: Update task fields (status, deadline, description) with ownership validation.
  - `DELETE /academic_tasks/{academic_tasks_id}`: Remove a task with ownership validation.
- Enforce strict ownership policies across all queries using `auth = "user"` and verifying `user_id == $auth.id`.
- Update the Streamlit frontend Disciplinas page (`pages/1_📚_Disciplinas.py`) to fetch from and persist data to Xano via authenticated requests.
- Update the Streamlit frontend Tarefas page (`pages/2_📝_Tarefas.py`) to fetch from and persist data to Xano via authenticated requests.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `academic-crud`: Refine and reinforce secure CRUD operations and data ownership constraints for subjects and academic tasks, including frontend synchronization.

## Impact

- **Backend / APIs**: Endpoints defined in `api/subjects/` and `api/academic_tasks/`.
- **Frontend / Streamlit**: `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` communicating with Xano endpoints using `Authorization: Bearer <token>`.
- **Database**: Relies on `table/subjects.xs` and `table/academic_tasks.xs` schemas with `user_id` foreign key.
- **Security**: All endpoints enforce `auth = "user"`, rejecting unauthenticated requests and queries targeting another student's data.

