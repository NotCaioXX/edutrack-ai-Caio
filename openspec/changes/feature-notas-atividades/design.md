# Design

## Context

EduTrack AI features a Streamlit frontend and a Xano backend architecture (`tables/`, `apis/`, `functions/`). Current tables include `user`, `account`, and `subjects`. See `proposal.md` for motivation and `specs/activity-grades/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Define database table schema `activity_grades` in XanoScript to persist student grades for academic activities.
- Implement API endpoint `POST /activity_grades` in XanoScript to record grade submissions by professors.

**Non-Goals:**
- Querying/listing endpoints (such as `GET /activity_grades` or `GET /academic_tasks/{id}/grades`), grade reports, or calculation formulas, in strict accordance with the requested scope defined in `AGENTS.md`.

## Decisions

### 1. Dedicated `activity_grades` Table
- **Decision**: Create table `activity_grades` with fields:
  - `id` (`int`, primary key)
  - `created_at` (`timestamp`, default `now`, visibility `"private"`)
  - `student_id` (`int`, foreign key referencing `user`)
  - `professor_id` (`int`, foreign key referencing `user`)
  - `task_id` (`int`, foreign key or identifier referencing the activity/task)
  - `grade` (`decimal`, filter: `min:0`, required)
  - `feedback` (`text`, optional, filter: `trim`)
- **Indexes**:
  - Primary key on `id`
  - B-tree index on `task_id` and `student_id`
- **Alternatives Considered**: Storing grades as an embedded JSON field inside tasks. Rejected because relational structure ensures data integrity and indexing.

### 2. Single Endpoint for Submitting Grades
- **Decision**: Provide `POST /activity_grades` to record new grade entries with authentication validation.
- **Alternatives Considered**: Batch grade submission endpoint. Deferred until explicitly requested.

## Risks / Trade-offs

- **[Risk] Unauthorized grade submission**: A student or unauthorized user submitting grades.
  - **Mitigation**: Backend endpoint enforces authentication and validates that the acting user has instructor/professor permissions.

## Migration Plan

1. Create `activity_grades` table schema file in `tables/activity_grades.xs`.
2. Create `POST /activity_grades` API endpoint in `apis/`.

