# Proposal

## Why

Students using EduTrack AI need the ability to register, track, and manage their academic obligations (assignments, exams, coursework, and homework) associated with each enrolled subject. Currently, the platform has subject tracking (`subjects` table) but lacks a dedicated data schema to store and organize academic tasks linked to those subjects. Creating the `academic_tasks` table provides the structured data foundation needed for students to manage deadlines and task statuses.

## What Changes

- Define and introduce the `academic_tasks` data model/table in XanoScript to store student obligations.
- Define table schema fields:
  - `id`: Unique primary key identifier (`int`).
  - `created_at`: Creation timestamp (`timestamp`, private visibility).
  - `user_id`: Reference to the authenticated student (`user` table).
  - `subject_id`: Reference to the academic subject (`subjects` table).
  - `title`: Title/headline of the task (`text`, trimmed).
  - `description`: Detailed instructions or notes for the task (`text`, optional, trimmed).
  - `due_date`: Target completion/deadline date (`date`, optional).
  - `status`: Lifecycle status of the task (e.g., 'pending', 'in_progress', 'completed') (`text`, trimmed).
- Establish primary and foreign key indexes for query performance (`id`, `user_id`, `subject_id`).

## Capabilities

### New Capabilities
- `academic-tasks`: Data schema and management for student academic tasks and obligations linked to enrolled subjects.

### Modified Capabilities
<!-- None -->

## Impact

- **Database / Schema**: Addition of `tables/academic_tasks.xs` referencing `subjects` and `user` tables.
- **Backend / APIs**: Sets the prerequisite schema for subsequent task management APIs.
- **Dependencies**: No external library additions required.

