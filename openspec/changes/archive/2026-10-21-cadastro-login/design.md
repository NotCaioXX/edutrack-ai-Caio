# Design

## Context

EduTrack AI's frontend is built with Streamlit (`app.py` and `pages/`). The backend provides Xano authentication endpoints under the `Authentication` API group:
- `POST /auth/signup`: Accepts `name`, `email`, `password`; creates a record in the `user` table and returns `{ authToken, user_id }`.
- `POST /auth/login`: Accepts `email`, `password`; validates credentials and returns `{ authToken }`.
- `GET /auth/me`: Requires `Authorization: Bearer <authToken>`; returns authenticated user details `{ id, created_at, name, email, account_id, role }`.

Currently, `pages/3_👤_Perfil.py` is empty, and `.env` is unconfigured.

## Goals / Non-Goals

**Goals:**
- Provide a `.env` file at the project root defining `XANO_AUTH_BASE_URL`.
- Implement `pages/3_👤_Perfil.py` with registration, login, profile inspection, and logout functionality.
- Manage authentication tokens and user state cleanly via `st.session_state`.
- Provide error handling for network issues, invalid credentials, and duplicate registrations.

**Non-Goals:**
- Modifying backend XanoScript files (existing authentication endpoints are already defined in `api/authentication/auth/`).
- Password reset flows via email or magic links.

## Decisions

### 1. Environment Configuration in `.env`
- **Decision**: Define `XANO_AUTH_BASE_URL` in `.env` located at the project root.
- **Rationale**: Keeps backend URLs configurable across environments without hardcoding API endpoints in code.
- **Implementation**: Read variables using a helper function supporting both `.env` file parsing and environment variables.

### 2. Streamlit Session State Management
- **Decision**: Store authentication state in `st.session_state["auth_token"]` and `st.session_state["user_info"]`.
- **Rationale**: Streamlit re-executes scripts on user interaction; session state ensures the user remains logged in across navigation between pages.

### 3. UI Layout and User Experience
- **Decision**: When unauthenticated, display two tabs: "🔑 Entrar (Login)" and "📝 Cadastrar (Cadastro)". When authenticated, display user profile information (name, email, role) with an option to log out ("🚪 Sair").
- **Rationale**: Standard, intuitive authentication UX tailored to single-page Streamlit multi-page navigation.

## Risks / Trade-offs

- **[Risk] Missing or invalid `.env` configuration**: If `XANO_AUTH_BASE_URL` is empty or unreachable, API requests will fail.
  - **Mitigation**: Add validation in `3_👤_Perfil.py` to notify the user with `st.warning` if the backend URL is not configured.
- **[Risk] Network timeout or connection errors**:
  - **Mitigation**: Wrap API requests in `try...except requests.exceptions.RequestException` blocks with user-friendly error banners.

## Migration Plan

1. Define `XANO_AUTH_BASE_URL` in `.env`.
2. Implement the authentication logic and UI components in `pages/3_👤_Perfil.py`.
3. Verify signup, login, profile view, and logout flows.
