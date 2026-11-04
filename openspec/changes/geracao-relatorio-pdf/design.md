# Design

## Context

EduTrack AI manages student subjects and academic tasks via CRUD endpoints, and computes completion metrics through `scripts/calculate_progress.py`. To fulfill reporting requirements, a dedicated script is needed to assemble performance data into an exportable, cleanly styled PDF report document, and an authenticated Xano endpoint is needed to permit secure retrieval and download of this report. See `proposal.md` for background and `specs/pdf-report/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Implement `scripts/generate_pdf_report.py` to create formatted PDF performance reports.
- Support data retrieval directly from Xano CRUD endpoints or local calculation functions.
- Present clean layout: Header (EduTrack AI, student name, date), Summary cards (total subjects, total tasks, overall completion rate), and Subject Breakdown table.
- Define an authenticated XanoScript endpoint `GET /reports/performance_pdf` in `api/reports/` with `auth = "user"` ensuring only the authenticated user can access their report.
- Support both programmatic invocation (importable function) and CLI execution (`python scripts/generate_pdf_report.py --output ...`).

**Non-Goals:**
- Automatic execution of push/deploy tools to Xano, strictly respecting Rule #2 in `AGENTS.md`.
- Modifying underlying database table schemas (`user`, `subjects`, `academic_tasks`).
- Sending automated emails or push notifications.

## Decisions

### 1. PDF Generation Engine: `fpdf2`
- **Decision**: Use `fpdf2` as the PDF rendering library.
- **Rationale**: `fpdf2` is modern, lightweight, pure Python, has no C/system-level dependencies (unlike WeasyPrint or wkhtmltopdf), and integrates seamlessly on Windows.
- **Alternatives Considered**:
  - `reportlab`: Heavier, more complex boilerplate for simple documents.
  - `weasyprint`: Requires GTK and external native libraries that are difficult to manage on Windows environments.

### 2. Document Layout and Structure
- **Decision**: Design a clean, 1-page (or multi-page if many subjects) portrait A4 document:
  - Header: Application title, generation timestamp, student name/email.
  - Metrics Summary: Total subjects, overall tasks, completed tasks, overall progress %.
  - Details Table: Subject name, teacher, total tasks, completed, progress %.
- **Rationale**: Clean, readable, and professional academic look.

### 3. Backend Endpoint: `GET /reports/performance_pdf`
- **Decision**: Create an API group `Reports` under `api/reports/` containing `api_group.xs` and `reports_performance_pdf_GET.xs`.
- **Security**: Endpoint enforces `auth = "user"`, restricting output to the student's own records (`$auth.id`).
- **Rationale**: Follows standard RESTful practices established in `api/subjects/` and `api/academic_tasks/`.

### 4. Data Integration Strategy
- **Decision**: Leverage `scripts.calculate_progress.calculate_all_progress` to fetch and compute subject progress, ensuring consistency between JSON reporting and PDF reports.
- **Rationale**: Avoids code duplication and guarantees metrics in the PDF match the calculation logic exactly.

## Risks / Trade-offs

- **[Risk] Missing `reports/` output folder**:
  - **Mitigation**: Automatically create the destination directory (`os.makedirs(..., exist_ok=True)`) before writing the PDF file.
- **[Risk] Unicode characters (emojis / accents in Portuguese)**:
  - **Mitigation**: Use standard fonts with proper character encoding handling, avoiding bare unsupported emoji in PDF text streams.

## Migration Plan

1. Add `fpdf2` to `requirements.txt`.
2. Define API group and endpoint in `api/reports/`.
3. Implement `scripts/generate_pdf_report.py`.
4. Verify PDF generation and output integrity.
