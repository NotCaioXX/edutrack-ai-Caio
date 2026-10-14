# Spec Delta

## Purpose

Enables professors in EduTrack AI to record and assign grades to students for specific academic activities.

## ADDED Requirements

### Requirement: Submit Activity Grade
The system SHALL allow an authenticated professor to submit a grade for a student on a specific academic activity, including numeric score and optional feedback.

#### Scenario: Successful grade submission
- **WHEN** the professor submits a valid grade and student identifier for a specific activity
- **THEN** the system records the grade and associates it with the activity and student record

#### Scenario: Missing required grade score
- **WHEN** the professor submits a grade entry without specifying the numeric grade value
- **THEN** the system rejects the submission with a validation error indicating the grade value is required

