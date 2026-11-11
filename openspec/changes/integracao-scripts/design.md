# Design

## Context

EduTrack AI features Python scripts for progress calculation (`scripts/calculate_progress.py`) and PDF report rendering (`scripts/generate_pdf_report.py`). The Streamlit application currently includes pages for Disciplinas, Tarefas, and Perfil. This design introduces `pages/4_📊_Progresso.py` to seamlessly unite the existing CLI/module scripts into the web interface. See `proposal.md` for motivation and `specs/scripts-integration/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Create `pages/4_📊_Progresso.py` conforming to Streamlit multi-page standards and page naming conventions.
- Call `calculate_all_progress(token=...)` from `scripts/calculate_progress.py` to obtain live metrics.
- Display visual metrics: overall completion rate metric, individual subject progress bars (`st.progress`), and task status breakdowns.
- Provide a responsive download button (`st.download_button`) using `generate_performance_pdf()` from `scripts/generate_pdf_report.py`.
- Enforce authentication check matching existing pages (`st.session_state["auth_token"]`).

**Non-Goals:**
- Creating new database tables or backend Xano endpoints.
- Modifying calculation algorithms or PDF layouts already established.
- Pushing or deploying changes to Xano servers (Rule #2).

## Decisions

### 1. New Streamlit Page: `pages/4_📊_Progresso.py`
- **Decision**: Follow existing numbered naming pattern (`1_📚_Disciplinas.py`, `2_📝_Tarefas.py`, `3_👤_Perfil.py`) with `4_📊_Progresso.py`.
- **Rationale**: Streamlit automatically recognizes numbered prefixes for sidebar navigation sorting.

### 2. Direct Script Module Consumption
- **Decision**: Import and invoke functions directly from `scripts.calculate_progress` and `scripts.generate_pdf_report`:
  - `calculate_all_progress(token=token)`
  - `generate_performance_pdf(student_name=..., student_email=..., token=token, output_path=...)`
- **Rationale**: Direct module import avoids spawning subprocesses, ensuring high performance, easy error propagation, and clean code reuse.

### 3. PDF Download via `st.download_button`
- **Decision**: Read the generated PDF binary bytes and pass them to Streamlit's native `st.download_button(label="📥 Baixar Relatório em PDF", data=pdf_bytes, file_name="relatorio_desempenho.pdf", mime="application/pdf")`.
- **Rationale**: Provides an immediate, clean in-browser download experience without opening external viewer windows.

## Risks / Trade-offs

- **[Risk] Unauthenticated user attempt**:
  - **Mitigation**: Display informative banner redirecting to Perfil page; disable PDF generation until logged in.
- **[Risk] Temporary file clutter**:
  - **Mitigation**: Use designated output path in `reports/` and reuse or stream bytes directly.

## Migration Plan

1. Create `pages/4_📊_Progresso.py`.
2. Connect script imports and session state handling.
3. Validate page rendering and PDF download in Streamlit.

