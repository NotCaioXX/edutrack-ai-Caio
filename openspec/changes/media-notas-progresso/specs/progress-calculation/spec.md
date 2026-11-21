# progress-calculation Specification

## ADDED Requirements

### Requirement: Cálculo e exibição de média de notas de tarefas
The system SHALL calculate the average grade of completed tasks with assigned grades for each subject and globally, displaying the average grade on the progress page and within the exported PDF performance report.

#### Scenario: Subject has completed tasks with grades
- **WHEN** calculating metrics for a subject having completed tasks with assigned grade values
- **THEN** the system computes the arithmetic average grade rounded to two decimal places and provides `average_grade` and `graded_tasks` count

#### Scenario: Subject has no graded tasks
- **WHEN** calculating metrics for a subject with no graded tasks
- **THEN** the system returns `average_grade` as null and handles display gracefully without division by zero errors

#### Scenario: Exporting PDF report with task grades
- **WHEN** the user generates and downloads the performance report PDF
- **THEN** the PDF includes overall average grade in executive summary metrics and an average grade column in the subjects detail table
