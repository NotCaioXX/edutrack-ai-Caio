# progress-calculation Specification

## Purpose

Enables computation and structured JSON reporting of student task completion percentages for academic subjects in EduTrack AI.

## ADDED Requirements

### Requirement: Calculate Subject Task Progress
The system SHALL calculate the completion progress percentage for an academic subject by dividing the count of completed tasks by the total count of tasks for that subject and multiplying by 100.

#### Scenario: Subject with completed and pending tasks
- **WHEN** calculating progress for a subject with 2 completed tasks out of 4 total tasks
- **THEN** the system calculates a progress percentage of 50.0

#### Scenario: Subject with no tasks
- **WHEN** calculating progress for a subject with 0 total tasks
- **THEN** the system returns a progress percentage of 0.0 without division by zero errors

#### Scenario: All tasks completed
- **WHEN** calculating progress for a subject where all 3 tasks are marked as completed
- **THEN** the system calculates a progress percentage of 100.0

### Requirement: Structured JSON Output
The system SHALL format and return the calculated progress information as a structured JSON object containing subject identification, task totals, completed count, and the computed progress percentage.

#### Scenario: JSON output structure validation
- **WHEN** progress calculation completes for a subject
- **THEN** the system produces a JSON payload containing `subject_id`, `total_tasks`, `completed_tasks`, and `progress_percentage`

### Requirement: Consume CRUD Endpoints for Data Fetching
The system SHALL retrieve subjects and associated tasks directly from the authenticated CRUD endpoints to perform the progress calculation.

#### Scenario: Fetch data from CRUD endpoints
- **WHEN** the calculation script executes with valid API configuration
- **THEN** the system queries `GET /subjects` and `GET /academic_tasks` to gather the live records for computation

