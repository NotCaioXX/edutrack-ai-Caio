# pdf-report Specification

## Purpose

Enables the generation, export, and secure backend download of structured academic performance reports in PDF format for students in EduTrack AI.

## ADDED Requirements

### Requirement: Generate Academic Performance PDF Report
The system SHALL generate a formatted PDF document compiling the student's academic performance metrics, including enrolled subjects, task completion counters, and computed progress percentages.

#### Scenario: Successful PDF report generation
- **WHEN** the report generation script is executed with valid student academic data
- **THEN** the system compiles the performance metrics and writes a valid PDF document to disk

#### Scenario: Performance breakdown per subject
- **WHEN** the PDF report document is generated
- **THEN** the output contains a detailed breakdown for each subject displaying subject name, total tasks, completed tasks, pending tasks, and completion percentage

#### Scenario: Overall progress summary inclusion
- **WHEN** rendering the PDF report
- **THEN** the document displays an executive summary section containing overall academic completion percentage across all subjects

### Requirement: Configurable Output Path and Parameters
The system SHALL allow specifying the destination file path for the generated PDF document via function arguments or CLI parameters, with fallback to a default location.

#### Scenario: Custom output destination specified
- **WHEN** the user specifies a custom file path for the generated report
- **THEN** the system writes the PDF document to the specified file path

#### Scenario: Default output destination fallback
- **WHEN** no output path is explicitly supplied
- **THEN** the system saves the report to a default path within the `reports/` directory

### Requirement: Authenticated Xano Report Download Endpoint
The system SHALL provide an authenticated backend endpoint in Xano allowing students to retrieve and download their generated academic performance report.

#### Scenario: Authenticated student requests report download
- **WHEN** an authenticated user sends a request to `GET /reports/performance_pdf`
- **THEN** the system validates that the user is authenticated and returns the report file or payload scoped to that student

#### Scenario: Unauthenticated request to download report
- **WHEN** an unauthenticated request is submitted to the report download endpoint
- **THEN** the system rejects the request with an access denied or unauthorized error
