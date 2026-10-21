# Proposal

## Why

EduTrack AI currently lacks an interface for users to sign up, authenticate, and view their user profile in the Streamlit application. While the Xano backend already provides authentication endpoints (`auth/signup`, `auth/login`, and `auth/me`) and the `user` table, the frontend page `pages/3_👤_Perfil.py` is empty and does not allow users to register or log into the platform. Providing authentication on the profile page enables students and instructors to register accounts, authenticate securely, and manage their session state across the app.

## What Changes

- Configure the base URL for Xano authentication endpoints inside a `.env` file at the project root.
- Implement the Streamlit authentication interface in `pages/3_👤_Perfil.py` supporting:
  - User registration (signup) calling `POST /auth/signup` and saving records into the `user` table.
  - User authentication (login) calling `POST /auth/login` and obtaining the JWT authentication token.
  - Profile view displaying authenticated user details retrieved via `GET /auth/me`.
  - Session state persistence in Streamlit to maintain user login state.

## Capabilities

### New Capabilities
- `user-profile-auth`: User registration, authentication, and session profile management in the Streamlit frontend using Xano authentication endpoints.

### Modified Capabilities
<!-- None -->

## Impact

- **Configuration**: Addition of `XANO_API_BASE_URL` (or equivalent base URL) in `.env` at the project root.
- **Frontend**: Full implementation of `pages/3_👤_Perfil.py` with signup, login, and profile views.
- **Backend / APIs**: Consumes existing `auth/signup`, `auth/login`, and `auth/me` endpoints from the `Authentication` API group.
- **Dependencies**: Uses `requests` and Streamlit session state (already installed in the environment).
