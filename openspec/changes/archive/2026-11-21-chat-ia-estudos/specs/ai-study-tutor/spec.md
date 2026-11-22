# ai-study-tutor Specification

## Purpose
Prover uma interface de chat interativa com inteligência artificial para que os estudantes possam tirar dúvidas sobre estudos, rotinas e novas técnicas de aprendizagem.

## ADDED Requirements

### Requirement: Conversação interativa com assistente de estudos
The system SHALL provide a dedicated chat page where the user can send messages about their studies and receive responses from an AI tutor.

#### Scenario: User sends a question about study techniques
- **WHEN** user submits a question or request in the chat input
- **THEN** system stores the user message in session history, queries the AI service, and displays the response in the conversation flow

#### Scenario: Maintaining conversation history in current session
- **WHEN** user exchanges multiple messages with the AI tutor
- **THEN** system maintains the full dialogue history in the current session state so the conversation remains contextual

### Requirement: Integração com provedor de IA e system prompt educacional
The system SHALL communicate with the AI model using a pre-configured API key and a specialized system instruction focused on study strategies and academic productivity.

#### Scenario: AI responds using study-focused persona
- **WHEN** the AI tutor generates an answer
- **THEN** the response reflects clear guidance on study techniques (e.g., Feynman, Pomodoro, Active Recall) and academic support in Brazilian Portuguese

#### Scenario: Handling missing API key or connection error
- **WHEN** the AI API key is not configured or an external service error occurs
- **THEN** the system SHALL display an informative notification guiding the user on how to configure the API key without crashing the application

### Requirement: Consulta automática de contexto acadêmico e notas
The system SHALL detect when user asks about grades, performance, or academic progress, fetching data from active session or guiding user to log in if unauthenticated.

#### Scenario: Authenticated user asks about grades or subjects
- **WHEN** user is logged in and asks about their grades or performance
- **THEN** system injects their current academic progress and grades context into the AI prompt to answer accurately

#### Scenario: Unauthenticated user asks about grades
- **WHEN** user is not logged in and asks about their personal grades
- **THEN** system guides the user to log in on the Perfil page so their academic records can be retrieved

### Requirement: Janela de chat com rolagem interna fixa
The system SHALL render the chat messages in a dedicated scrollable container with fixed height so the top navigation header remains easily accessible.

#### Scenario: Long conversation flow
- **WHEN** multiple messages are exchanged in the chat
- **THEN** the messages scroll inside a designated container with fixed max height and the navigation header stays readily reachable without extensive page scrolling
