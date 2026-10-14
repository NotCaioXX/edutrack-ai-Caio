# Design

## Context

EduTrack AI features a relational backend built on Xano with schema files located in `tables/`. Academic subjects are defined in `tables/subjects.xs` with foreign key relations to `user`. Students need a dedicated entity to store homework, assignments, and test dates linked to their enrolled subjects.

See `proposal.md` for motivation and `specs/academic-tasks/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Design the XanoScript schema for `academic_tasks` with strict type definitions and field filters.
- Define foreign key relationships to both `user` and `subjects` tables.
- Specify query indexes for primary lookups and relationship traversals.

**Non-Goals:**
- Backend API endpoint definitions (reserved for a dedicated API change).
- Streamlit UI task management screens (reserved for frontend integration).

## Decisions

### 1. Relational `academic_tasks` Table Schema
- **Decision**: Define table `academic_tasks` with the following schema structure:
  - `int id`: Unique primary key identifier.
  - `timestamp created_at?=now`: Auto-populated creation timestamp with `visibility = "private"`.
  - `int user_id`: Foreign key referencing table `"user"` (`table = "user"`).
  - `int subject_id`: Foreign key referencing table `"subjects"` (`table = "subjects"`).
  - `text title filters=trim`: Required task title with trim filter.
  - `text description? filters=trim`: Optional descriptive notes with trim filter.
  - `date due_date?`: Optional due date for the obligation.
  - `text status?="pending" filters=trim`: Current lifecycle state of the task with default `'pending'`.
- **Alternatives Considered**: Embedding tasks as an array inside `subjects.xs`. Rejected because independent tasks require individual deadlines, statuses, and querying across multiple subjects.

### 2. Index Strategy
- **Decision**:
  - `primary` on `id`
  - `btree` on `user_id` (enables scoped queries by student)
  - `btree` on `subject_id` (enables filtering tasks by subject)
- **Rationale**: Matches Xano best practices for indexed foreign keys.

## Risks / Trade-offs

- **[Risk] Foreign key dependency on `subjects`**: Tasks must not reference non-existent subjects.
  - **Mitigation**: Foreign key definition `table = "subjects"` ensures referential integrity in Xano.

## Migration Plan

1. Create `tables/academic_tasks.xs` adhering strictly to XanoScript syntax.
2. Validate file formatting against Xano language server parser.

