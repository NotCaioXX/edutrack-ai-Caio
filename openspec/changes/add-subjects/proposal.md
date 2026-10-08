# Proposal

## Why

EduTrack AI is an academic tracking assistant designed to help students organize their studies, academic tasks, and courses. Currently, the platform has a placeholder interface without the capability to manage academic subjects ("disciplinas"). Introducing the `subjects` capability allows students to register, list, update, and track their subjects, providing the foundational academic structure needed to organize tasks, calculate metrics, and display active disciplines on the dashboard.

## What Changes

- Add academic subject management data model (`subject` / `disciplina`) to store course information such as subject name, professor name, semester/term, color/tag, and active status.
- Provide backend CRUD API endpoints / data operations for subjects (create, read/list, update, delete).
- Integrate subject listing and management into the EduTrack AI interface (Streamlit frontend and dashboard metrics).
- Associate subjects with user accounts so each student manages their own academic course load.

## Capabilities

### New Capabilities
- `subjects`: Covers academic subject management including creating new subjects, retrieving subject lists, editing subject details, and tracking active course enrollment for students.

### Modified Capabilities
<!-- None -->

## Impact

- **Database / Schema**: Introduction of a `subject` table schema referencing user/account with fields for subject name, professor, semester, and status.
- **Backend / APIs**: Creation of API endpoints for listing, creating, updating, and deleting subjects.
- **Frontend**: `app.py` navigation under "Disciplinas" and "Dashboard" metrics updated to consume subject data dynamically.
- **Dependencies**: No external library additions required; integrates with existing Streamlit interface and Xano backend models.
