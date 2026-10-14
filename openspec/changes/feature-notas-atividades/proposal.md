# Proposal

## Why

In EduTrack AI, professors need the capability to record and assign grades to students for specific academic activities. Currently, the system lacks a data model and backend endpoint dedicated to storing and submitting grades for student activities. Introducing this capability allows instructors to submit student grades for specific tasks, establishing the foundational grading record in the application.

## What Changes

- Create a data schema for activity grades (`activity_grades` table) storing the association between student, academic task/activity, grade value, optional feedback, and assignment timestamp.
- Implement an API endpoint (`POST /activity_grades`) allowing authenticated instructors/professors to submit and record a student's grade for a specific activity.

## Capabilities

### New Capabilities
- `activity-grades`: Enables professors to record and submit student grades for specific academic activities.

### Modified Capabilities
<!-- None -->

## Impact

- **Database / Schema**: New `activity_grades` table referencing `user` (student), the authenticated professor, and the specific academic task/activity.
- **Backend / APIs**: New `POST /activity_grades` endpoint for grade submission with payload validation.
- **Frontend / Dependencies**: No additional third-party dependencies required.
