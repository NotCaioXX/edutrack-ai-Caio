# Design

## Context

EduTrack AI connects to backend Xano services using URLs configured for authentication, subjects, and tasks. Currently, each Streamlit page executes a custom `load_env()` function that manually reads a `.env` file into `os.environ`. Streamlit features built-in secret management via `st.secrets` backed by `.streamlit/secrets.toml`. This design outlines migrating configuration resolution to `st.secrets` while preserving fallback compatibility. See `proposal.md` for motivation and `specs/secrets-configuration/spec.md` for requirements.

## Goals / Non-Goals

**Goals:**
- Replace repetitive manual `.env` file parsing in Streamlit pages with `st.secrets`.
- Provide a unified configuration access pattern (`st.secrets.get(key) or os.environ.get(key)`).
- Maintain backward compatibility for standalone scripts executing outside Streamlit (`scripts/calculate_progress.py`, `scripts/generate_pdf_report.py`).
- Verify protection of `.streamlit/secrets.toml` in `.gitignore`.

**Non-Goals:**
- Changing database tables or Xano backend endpoints.
- Executing push or deployment commands (Rule #2).

## Decisions

### 1. Unified Configuration Helper
- **Decision**: Use a helper pattern across Streamlit pages:
  ```python
  def get_config(key: str, default: str = "") -> str:
      """Retrieves configuration primarily from st.secrets, falling back to os.environ."""
      try:
          if key in st.secrets:
              return str(st.secrets[key]).rstrip("/")
      except Exception:
          pass
      return os.environ.get(key, default).rstrip("/")
  ```
- **Rationale**: Safe against missing `.streamlit/secrets.toml` files, avoids throwing `KeyError`, and seamlessly supports both local and cloud deployment setups.

### 2. Standalone Script Compatibility
- **Decision**: Standalone scripts in `scripts/` check for `st.secrets` if `streamlit` is loaded; otherwise, they retain fallback loading from `.env` via `load_env()`.
- **Rationale**: Allows running scripts from terminal/CLI without requiring a Streamlit runtime while sharing the same configuration values.

## Risks / Trade-offs

- **[Risk] Missing `.streamlit/secrets.toml` file**:
  - **Mitigation**: Helper checks `key in st.secrets` within a `try/except` block and falls back to `os.environ`.
- **[Risk] Accidental secret commit to Git**:
  - **Mitigation**: `.gitignore` contains `.streamlit/` and `.env`.

## Migration Plan

1. Update `app.py` to use `st.secrets`.
2. Update `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_👤_Perfil.py`, and `pages/4_📊_Progresso.py`.
3. Ensure `scripts/calculate_progress.py` and `scripts/generate_pdf_report.py` maintain fallback.
4. Verify all pages compile and load configuration properly.
