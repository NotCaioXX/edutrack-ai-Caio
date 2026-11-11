# secrets-configuration Specification

## Purpose

Defines the secure retrieval, prioritization, and protection of backend configuration and API URLs using Streamlit native secrets in EduTrack AI.

## ADDED Requirements

### Requirement: Read Configuration from Streamlit Secrets
The system SHALL retrieve backend API URLs and authentication endpoints primarily from `st.secrets` within Streamlit runtime contexts.

#### Scenario: Configuration loaded from secrets.toml
- **WHEN** the Streamlit application starts with keys defined in `.streamlit/secrets.toml`
- **THEN** the system retrieves `XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL`, and `XANO_TASKS_BASE_URL` directly from `st.secrets`

#### Scenario: Fallback to environment variables
- **WHEN** a required configuration key is not present in `st.secrets` but exists in `os.environ`
- **THEN** the system resolves the value from `os.environ` without raising exceptions

### Requirement: Protection of Secrets in Version Control
The system SHALL ensure that local secrets files are excluded from Git version control.

#### Scenario: Local secrets excluded from repository
- **WHEN** inspecting the repository status with Git
- **THEN** both `.streamlit/` and `.env` are ignored by `.gitignore` and not tracked in commits
