# activity-grades Specification

## Purpose
Permite que os estudantes registrem, editem e consultem notas atribuídas a tarefas e atividades acadêmicas concluídas no EduTrack AI.

## Requirements

### Requirement: Registro de nota em atividades concluídas
The system SHALL allow users to assign and persist a numeric grade (between 0.0 and 10.0) to academic tasks that are marked with completed status.

#### Scenario: User submits a valid grade for a completed task
- **WHEN** user inputs a valid grade for an activity with completed status
- **THEN** the system updates the task record persisting the grade value in the database

#### Scenario: User attempts to assign an out-of-range grade
- **WHEN** user enters a grade value outside the range of 0.0 to 10.0
- **THEN** the system rejects the input or clamps the value, indicating the acceptable range

### Requirement: Exibição visual da nota no card da tarefa
The system SHALL display the recorded grade within the academic task card interface in the frontend for completed tasks, maintaining the application design standards without emojis.

#### Scenario: Completed task with assigned grade is displayed
- **WHEN** the user views a completed task that has an assigned grade
- **THEN** the system displays the grade clearly formatted within the task details

#### Scenario: Completed task without assigned grade
- **WHEN** the user views a completed task that does not have an assigned grade
- **THEN** the system displays an indicator that the task is pending grade entry
