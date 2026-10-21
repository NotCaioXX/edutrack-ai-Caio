# Spec Delta

## Purpose

Enables users to register new accounts, authenticate, and manage their session profile within the EduTrack AI Streamlit application using Xano authentication endpoints.

## ADDED Requirements

### Requirement: User Registration
The system SHALL provide a registration form allowing users to submit name, email, and password to create an account via the `POST /auth/signup` endpoint.

#### Scenario: Successful user registration
- **WHEN** the user submits valid name, email, and password on the registration form
- **THEN** the system creates the user record in the database, stores the returned authentication token in the session, and presents a success message

#### Scenario: Registration with duplicate email
- **WHEN** the user attempts to register with an email address already registered in the system
- **THEN** the system presents an error message indicating the account is already in use

### Requirement: User Authentication
The system SHALL provide a login form allowing registered users to authenticate by submitting email and password to the `POST /auth/login` endpoint.

#### Scenario: Successful login
- **WHEN** the user submits valid email and password credentials
- **THEN** the system authenticates the user, stores the authentication token in session state, and redirects to the authenticated profile view

#### Scenario: Invalid login credentials
- **WHEN** the user submits an incorrect email or password
- **THEN** the system rejects authentication and displays an invalid credentials error message

### Requirement: Authenticated User Profile Display
The system SHALL fetch and display the authenticated user's information from `GET /auth/me` when an active authentication token exists in session state.

#### Scenario: View authenticated profile
- **WHEN** an authenticated user accesses the profile page with a valid session token
- **THEN** the system displays the user's name, email, and account details retrieved from the backend

#### Scenario: User logout
- **WHEN** an authenticated user clicks the logout button
- **THEN** the system clears the authentication token from session state and renders the login and registration forms
