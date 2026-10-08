# Spec Delta

## Purpose

Enables students using EduTrack AI to manage their academic subjects (disciplinas), tracking course details, professors, terms, and enrollment status.

## ADDED Requirements

### Requirement: Create Academic Subject
The system SHALL allow users to register a new academic subject with details including name, professor name, semester, and enrollment status.

#### Scenario: Successful subject creation
- **WHEN** the user submits valid subject details with a required subject name
- **THEN** the system creates the subject record and associates it with the user's account

#### Scenario: Missing required subject name
- **WHEN** the user attempts to create a subject without providing a subject name
- **THEN** the system rejects the submission with a validation error indicating the name is required

### Requirement: List User Subjects
The system SHALL allow users to view all academic subjects associated with their account.

#### Scenario: View subjects list
- **WHEN** the user navigates to the subjects list
- **THEN** the system displays all registered subjects for the current user with their details and current status

#### Scenario: Empty subjects state
- **WHEN** the user has no registered academic subjects
- **THEN** the system presents a friendly message indicating no subjects have been registered yet

### Requirement: Update Subject Information
The system SHALL allow users to edit the information of an existing academic subject that belongs to their account.

#### Scenario: Successful subject update
- **WHEN** the user modifies the subject information such as professor, semester, or status and submits the update
- **THEN** the system updates the record and displays the updated information

### Requirement: Delete Subject
The system SHALL allow users to remove an existing academic subject from their account.

#### Scenario: Successful subject deletion
- **WHEN** the user confirms deletion of a subject
- **THEN** the system removes the subject record from the database and updates the subjects list

### Requirement: Display Active Subjects Metrics
The system SHALL calculate and display the number of active academic subjects on the dashboard metrics.

#### Scenario: Dashboard active disciplines metric
- **WHEN** the user views the dashboard
- **THEN** the system shows the accurate count of currently active academic subjects
