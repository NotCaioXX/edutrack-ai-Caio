# Design

## Context

EduTrack AI manages subjects and academic tasks stored in Xano through authenticated CRUD endpoints (`GET /subjects`, `GET /academic_tasks`). To provide visibility into student academic progress, a calculation mechanism is needed to compute task completion metrics per discipline. See `proposal.md` for motivation and `specs/progress-calculation/spec.md` for functional requirements.

## Goals / Non-Goals

**Goals:**
- Implement a Python module and CLI script in `scripts/calculate_progress.py`.
- Connect to the Xano CRUD endpoints to retrieve subjects and tasks using auth tokens or environment configuration.
- Implement calculation formula: `(completed_tasks / total_tasks) * 100` rounded to two decimal places.
- Gracefully handle zero tasks (`total_tasks == 0`) by returning `0.0` percentage.
- Return structured JSON representation of the computed metrics.

**Non-Goals:**
- Modifying database schemas or backend XanoScript files.
- Automatically running push/deploy commands (Rule #2).
- Adding complex graphical charts or reporting engines not requested.

## Decisions

### 1. Dual Execution Interface (Module & CLI)
- **Decision**: Structure `scripts/calculate_progress.py` so functions like `calculate_progress(tasks)` and `get_subject_progress(subject_id, token, base_url)` can be imported by other Python scripts, while `if __name__ == "__main__":` allows standalone execution from the command line.
- **Rationale**: Enables reuse in future Streamlit pages or background tasks while fulfilling the standalone script requirement.

### 2. Output Schema
- **Decision**: Return a JSON structure:
  ```json
  {
    "subject_id": 1,
    "subject_name": "Algoritmos",
    "total_tasks": 4,
    "completed_tasks": 2,
    "pending_tasks": 2,
    "progress_percentage": 50.0
  }
  ```
- **Rationale**: Simple, human-readable, and easily consumable by frontend applications or APIs.

### 3. Safe Math Handling
- **Decision**: Check `if total_tasks == 0: progress = 0.0` before performing division.
- **Rationale**: Prevents unexpected `ZeroDivisionError` when a student creates a discipline but has not yet added any assignments.

## Risks / Trade-offs

- **[Risk] Unauthenticated or missing token**:
  - **Mitigation**: Allow loading token from `.env` or passing as an argument, and provide clear error messages if authentication fails.
- **[Risk] Status values variability**:
  - **Mitigation**: Consider tasks completed when `task.get("status") == "completed"`, adhering to the standard status vocabulary used across the application.

## Migration Plan

1. Create `scripts/` directory if not present.
2. Implement `scripts/calculate_progress.py`.
3. Verify calculation logic with edge cases (empty tasks, all completed, partial completed).

