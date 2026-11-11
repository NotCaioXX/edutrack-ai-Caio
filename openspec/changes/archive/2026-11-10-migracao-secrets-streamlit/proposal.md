# Proposal

## Why

EduTrack AI currently relies on manual parsing of `.env` files via custom `load_env()` functions across Streamlit pages to obtain backend URLs and authentication settings. Streamlit provides native, secure, and production-ready secret management through `st.secrets` (`.streamlit/secrets.toml`). Migrating from manual `.env` reading to Streamlit secrets simplifies configuration, enhances credential security, ensures compatibility with cloud deployments (such as Streamlit Community Cloud), and prevents secrets from leaking into version control.

## What Changes

- Migrate configuration loading across all Streamlit pages (`app.py`, `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_👤_Perfil.py`, `pages/4_📊_Progresso.py`) to use Streamlit's native `st.secrets`.
- Provide a robust resolution mechanism that retrieves configuration from `st.secrets` with fallback to `os.environ` / `.env`.
- Ensure standalone CLI scripts (`scripts/calculate_progress.py`, `scripts/generate_pdf_report.py`) maintain compatibility and graceful fallback.
- Verify that secret files (`.streamlit/secrets.toml` and `.env`) remain properly protected and ignored in `.gitignore`.

## Capabilities

### New Capabilities
- `secrets-configuration`: Manages application configuration and API URLs using Streamlit native secrets (`st.secrets`) with resilient fallback to environment variables.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend / Streamlit**: `app.py` and all files in `pages/` read settings directly from `st.secrets`.
- **Scripts**: Standalone scripts in `scripts/` maintain fallback to `.env` / `os.environ`.
- **Security**: Aligns with official Streamlit secrets standards and ensures secrets are excluded from Git.
