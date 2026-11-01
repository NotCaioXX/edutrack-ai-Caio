# Spec Delta

## MODIFIED Requirements

### Requirement: Secure Subject CRUD Operations
The system SHALL provide authenticated endpoints to create, list, retrieve, update, and delete subjects, ensuring each student only accesses and modifies their own subject records.

#### Scenario: User queries own subjects
- **WHEN** an authenticated student requests their subjects list via `GET /subjects`
- **THEN** the system returns only subjects where `user_id` matches the authenticated user

#### Scenario: User attempts to access another student's subject
- **WHEN** a user attempts to retrieve, modify, or delete a subject belonging to another user
- **THEN** the system rejects the request with an access denied or not found error

#### Scenario: Create subject with authenticated user association
- **WHEN** an authenticated user creates a subject via `POST /subjects`
- **THEN** the record is created with `user_id` mapped to the authenticated user ID

### Requirement: Secure Academic Task CRUD Operations
The system SHALL provide authenticated endpoints to create, list, retrieve, update, and delete academic tasks, ensuring each student only accesses and modifies their own tasks.

#### Scenario: User queries own academic tasks
- **WHEN** an authenticated student requests their tasks list via `GET /academic_tasks`
- **THEN** the system returns only tasks where `user_id` matches the authenticated user

#### Scenario: User attempts to modify another student's task
- **WHEN** a user attempts to update or delete a task belonging to a different user
- **THEN** the system rejects the operation with an access denied error

#### Scenario: Create task linked to subject and user
- **WHEN** an authenticated user creates a task via `POST /academic_tasks`
- **THEN** the system records the task with `user_id` mapped to the authenticated user and links it to the specified `subject_id`

## ADDED Requirements

### Requirement: Streamlit Subject and Task Persistence in Xano
The system SHALL synchronize subjects and academic tasks in the Streamlit frontend directly with the Xano API endpoints, ensuring data is saved to and retrieved from Xano under the authenticated user session.

#### Scenario: User views and manages subjects in Streamlit
- **WHEN** an authenticated user opens the Disciplinas page in Streamlit
- **THEN** the application queries `GET /subjects` from Xano with the user auth token and renders the saved records

#### Scenario: User saves a new subject in Streamlit
- **WHEN** an authenticated user submits the new subject form
- **THEN** the application sends a `POST /subjects` request to Xano and updates the display upon success

#### Scenario: User views and creates tasks in Streamlit
- **WHEN** an authenticated user opens or submits a new task in the Tarefas page
- **THEN** the application communicates with `GET /academic_tasks` and `POST /academic_tasks` on Xano to persist and fetch tasks for that user

