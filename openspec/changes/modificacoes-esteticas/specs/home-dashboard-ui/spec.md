# Spec Delta

## Purpose

Provides home dashboard layout enhancements including top-right profile navigation, an upcoming tasks calendar with associated subjects list, and an overview of incomplete subjects progress.

## ADDED Requirements

### Requirement: Top-Right Profile Navigation
The system SHALL display a profile shortcut in the top-right corner of the home page redirecting to the user profile screen.

#### Scenario: User clicks profile shortcut
- **WHEN** the user views the home page
- **THEN** a link or button to the Profile screen is rendered in the top-right area, displaying the user's name or login prompt

### Requirement: Upcoming Tasks Delivery Calendar and Subjects List
The system SHALL display a calendar on the home screen with upcoming activity due dates and a list below it showing each subject included in this calendar.

#### Scenario: View calendar with upcoming due dates
- **WHEN** the home page loads with registered academic tasks having due dates
- **THEN** a calendar view displays the dates of upcoming deliverables and lists each associated subject with its upcoming tasks below the calendar

#### Scenario: No upcoming activities scheduled
- **WHEN** there are no pending tasks with scheduled deadlines
- **THEN** the calendar shows the current month and an informative message indicates no upcoming deliveries are scheduled

### Requirement: Incomplete Subjects Progress Overview
The system SHALL display an overview card or panel showing the progress percentage of each academic subject that is not complete.

#### Scenario: Display incomplete subjects progress
- **WHEN** the user views the home page and has registered subjects with progress under 100%
- **THEN** the overview panel presents each incomplete subject with its calculated progress and visual progress indicator

#### Scenario: All subjects completed or no subjects
- **WHEN** all registered subjects have reached 100% completion or no subjects exist
- **THEN** the panel informs that all subjects are up to date or prompts to add new subjects
