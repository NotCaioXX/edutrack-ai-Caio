# Spec Delta

## Purpose

Enables students using EduTrack AI to record, organize, and track academic obligations such as homework, exams, and projects linked to their academic subjects.

## ADDED Requirements

### Requirement: Store Academic Task Record
The system SHALL persist academic task records containing an identifier, owner user reference, subject reference, title, optional description, optional due date, and status.

#### Scenario: Valid academic task creation
- **WHEN** a task record is submitted with a valid title, subject reference, and user reference
- **THEN** the database stores the academic task linked to the corresponding subject and user

#### Scenario: Missing required task title
- **WHEN** a task record is created without a title
- **THEN** the system rejects the task creation indicating the title is required

### Requirement: Academic Task Relationship to Subject
The system SHALL maintain a relational foreign key link between each academic task and its corresponding subject.

#### Scenario: Query tasks by subject
- **WHEN** querying tasks associated with a specific subject identifier
- **THEN** the database filters and returns the academic tasks referencing that subject_id

