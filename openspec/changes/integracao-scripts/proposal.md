# Proposal

## Why

EduTrack AI now contains functional backend CRUD endpoints and calculation/reporting utilities (`scripts/calculate_progress.py` and `scripts/generate_pdf_report.py`), but students currently have no dedicated interface in the Streamlit application to visualize their subject completion rates or export their PDF performance reports. Introducing a dedicated frontend page connects these scripts directly to the student UI, enabling interactive visual tracking and one-click PDF downloading.

## What Changes

- Create a new Streamlit page `pages/4_📊_Progresso.py` integrated into the application navigation.
- Use `scripts/calculate_progress.py` to calculate and render completion metrics and progress bars for each academic subject.
- Use `scripts/generate_pdf_report.py` to generate and provide a direct download button (`st.download_button`) for the student's academic performance report in PDF format.
- Integrate session authentication state to ensure calculations and report generation are scoped to the logged-in student.

## Capabilities

### New Capabilities
- `scripts-integration`: Provides a user interface in Streamlit to compute and display subject progress via `calculate_progress.py` and download performance PDF reports via `generate_pdf_report.py`.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend / Streamlit**: New page `pages/4_📊_Progresso.py` integrated with session state and navigation.
- **Scripts**: Consumes existing `scripts/calculate_progress.py` and `scripts/generate_pdf_report.py` modules.
- **Dependencies**: No additional external dependencies required (`streamlit` and `fpdf2` already present).

