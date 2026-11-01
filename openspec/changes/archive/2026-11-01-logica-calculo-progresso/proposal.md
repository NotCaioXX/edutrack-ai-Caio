# Proposal

## Why

EduTrack AI provides students with subjects and academic tasks, but currently lacks an automated mechanism to calculate and report task completion progress for academic subjects. Introducing a dedicated Python calculation script in `scripts/calculate_progress.py` allows students and instructors to quantify progress per subject (completed tasks divided by total tasks) and consume this information as structured JSON.

## What Changes

- Create `scripts/calculate_progress.py` implementing progress calculation logic for academic subjects based on their associated tasks.
- Integrate with existing CRUD endpoints (`GET /subjects` and `GET /academic_tasks`) to retrieve subject and task data.
- Calculate completion percentage `(completed_tasks / total_tasks) * 100` with safe zero-division handling when no tasks exist.
- Output results as structured JSON containing subject identifier, total tasks, completed tasks, and progress percentage.

## Capabilities

### New Capabilities
- `progress-calculation`: Calculates task completion percentages for academic subjects based on CRUD endpoint data and returns structured JSON output.

### Modified Capabilities
<!-- None -->

## Impact

- **Scripts**: Adds new script `scripts/calculate_progress.py`.
- **Backend / APIs**: Consumes existing `GET /subjects` and `GET /academic_tasks` CRUD endpoints.
- **Dependencies**: Relies on `requests` and Python standard library (`json`, `os`, `sys`). No new external packages required.

