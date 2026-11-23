# user-onboarding-access Specification

## Purpose
Gerenciar a experiência de introdução ao sistema para visitantes e novos usuários, bloqueando o acesso de usuários não logados a páginas restritas e exibindo mensagens de boas-vindas e primeiros passos.

## ADDED Requirements

### Requirement: Bloqueio de acesso para usuários não autenticados
The system SHALL restrict unauthenticated users to only the Home page and the Profile (authentication) page, blocking access to internal functional pages.

#### Scenario: Unauthenticated user accesses internal protected page
- **WHEN** an unauthenticated visitor accesses Disciplinas, Tarefas, Progresso, or Tutor IA
- **THEN** the system SHALL block the protected content and prompt the user to log in or create an account via the Perfil page

#### Scenario: Unauthenticated user uses top navbar
- **WHEN** an unauthenticated user views the top navigation bar
- **THEN** the system SHALL clearly indicate which actions require login or route them to the Perfil page

### Requirement: Tela de boas-vindas na Página Inicial para visitantes
The system SHALL display an introductory welcome screen on the Home page when the user is not authenticated.

#### Scenario: Visitor arrives at home page
- **WHEN** an unauthenticated user opens the Home page
- **THEN** the system SHALL display welcome information about EduTrack AI with call-to-action buttons to log in or register

### Requirement: Dashboard e onboarding para novos usuários logados
The system SHALL display the normal dashboard for authenticated users and show onboarding guidance when the user has no registered subjects or tasks.

#### Scenario: Authenticated user with existing records
- **WHEN** a logged-in user accesses the Home page with existing subjects and tasks
- **THEN** the system SHALL display the complete academic dashboard with metrics, calendar, and progress

#### Scenario: Newly registered user with zero subjects or tasks
- **WHEN** a logged-in user accesses the Home page and has no registered subjects
- **THEN** the system SHALL display an onboarding card guiding them to register their first subject and initial academic tasks
