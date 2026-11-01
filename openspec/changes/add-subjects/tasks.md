# Tasks

## 1. Database Schema

- [x] 1.1 Design and create the `subjects` table schema (`tables/subjects.xs`) with fields `id`, `name`, `teacher`, `hours`, `user_id` (FK to `user`), and indexes, verifying schema file format
- [x] 1.2 Verify table schema relationships with `user` and validate configuration for synchronization to Xano

## 2. Backend API Endpoints

- [x] 2.1 Implement `GET /subjects` endpoint to retrieve subjects belonging to the authenticated user and verify response payload structure
- [x] 2.2 Implement `POST /subjects` endpoint with input validation ensuring subject name is required, verifying successful record creation
- [x] 2.3 Implement `PATCH /subjects/{id}` and `DELETE /subjects/{id}` endpoints to support subject updates and deletions, verifying ownership checks

## 3. Frontend Integration (Streamlit)

- [x] 3.1 Update the "Disciplinas" section in `app.py` to render registered academic subjects with course name, professor, semester, and status badge
- [x] 3.2 Add a subject creation form in `app.py` with validation and user feedback upon successful addition
- [x] 3.3 Wire the "Disciplinas Ativas" metric on the Streamlit dashboard in `app.py` to reflect the count of active subjects dynamically

## 4. Verification

- [x] 4.1 Run Streamlit application locally and verify creating, listing, and counting academic subjects end-to-end

