# Proposal

## Why

Students and academic advisors in EduTrack AI need an exportable document summarizing student academic performance across all enrolled subjects, completed tasks, and pending deliverables. Currently, progress information is computed programmatically but cannot be exported as an official, shareable visual report or downloaded from the backend. Introducing a Python script to generate a structured PDF performance report, along with an authenticated Xano backend endpoint to download this report, fulfills this need by enabling automated PDF generation and secure cloud retrieval.

## What Changes

- Add a lightweight PDF generation library (`fpdf2`) to project dependencies.
- Create a Python script `scripts/generate_pdf_report.py` that aggregates academic performance data (subjects, task completion metrics, and progress percentages) and compiles a formatted PDF report.
- Create an authenticated Xano API endpoint (`GET /reports/performance_pdf`) in XanoScript to serve and allow students to download their performance report.
- Enforce strict authentication and multi-tenant isolation so students only download their own academic performance report.

## Capabilities

### New Capabilities
- `pdf-report`: Generates structured PDF performance reports compiling academic subjects, task completion metrics, and student progress summaries, with an authenticated Xano backend endpoint for downloading the document.

### Modified Capabilities
<!-- None -->

## Impact

- **Scripts**: New script `scripts/generate_pdf_report.py`.
- **Dependencies**: Adds `fpdf2` to `requirements.txt`.
- **Backend / APIs**: Creates a new endpoint in `api/reports/` in XanoScript (`GET /reports/performance_pdf`) with `auth = "user"`.
- **APIs / Data**: Consumes existing CRUD endpoints (`GET /subjects`, `GET /academic_tasks`, and calculation logic from `scripts/calculate_progress.py`).
