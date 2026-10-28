import os
from pathlib import Path
import streamlit as st
import requests

st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

def load_env():
    """Carrega as variáveis do arquivo .env localizado na raiz do projeto."""
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val

load_env()
BASE_URL = os.environ.get("XANO_API_BASE_URL") or os.environ.get("XANO_AUTH_BASE_URL", "").rstrip("/")

# Inicialização de variáveis de sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "cached_subjects" not in st.session_state:
    st.session_state["cached_subjects"] = []
if "cached_tasks" not in st.session_state:
    st.session_state["cached_tasks"] = []

token = st.session_state.get("auth_token")
user = st.session_state.get("user_info")

def get_auth_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}

def sync_dashboard_metrics():
    """Sincroniza contagens do Xano com tratamento resiliente."""
    subjects_count = len(st.session_state.get("cached_subjects", []))
    tasks_pending_count = sum(1 for t in st.session_state.get("cached_tasks", []) if t.get("status") != "completed")

    if BASE_URL:
        try:
            headers = get_auth_headers()
            user_id = user.get("id") if user else None
            params = {"user_id": user_id} if user_id else {}

            resp_subj = requests.get(f"{BASE_URL}/subjects", headers=headers, params=params, timeout=5)
            if resp_subj.status_code == 200 and isinstance(resp_subj.json(), list):
                st.session_state["cached_subjects"] = resp_subj.json()
                subjects_count = len(resp_subj.json())

            resp_tasks = requests.get(f"{BASE_URL}/academic_tasks", headers=headers, params=params, timeout=5)
            if resp_tasks.status_code == 200 and isinstance(resp_tasks.json(), list):
                st.session_state["cached_tasks"] = resp_tasks.json()
                tasks_pending_count = sum(1 for t in resp_tasks.json() if t.get("status") != "completed")
        except requests.exceptions.RequestException:
            pass

    return subjects_count, tasks_pending_count

# Título Principal
st.title("🎓 EduTrack AI")

if user:
    st.caption(f"Bem-vindo(a), **{user.get('name', 'Estudante')}**! Conectado ao Xano.")
else:
    st.caption("Visite a página **👤 Perfil** para autenticar-se e sincronizar dados com sua conta no Xano.")

st.markdown("---")

# Métricas Visuais Dinâmicas
subj_count, pending_count = sync_dashboard_metrics()

col1, col2 = st.columns(2)
col1.metric("Disciplinas Cadastradas (Tabela `subjects`)", str(subj_count))
col2.metric("Tarefas Pendentes (Tabela `academic_tasks`)", str(pending_count))

st.markdown("---")

st.subheader("🚀 Acesso Rápido")
st.markdown("""
Utilize a barra lateral para navegar pelo aplicativo:
- 📚 **Disciplinas**: Cadastre matérias com professor e carga horária (sincronizado com `tables/subjects.xs`).
- 📝 **Tarefas**: Gerencie lições, provas e entregas vinculadas a cada disciplina (sincronizado com `tables/academic_tasks.xs`).
- 👤 **Perfil**: Faça cadastro ou login na plataforma utilizando os endpoints de autenticação do Xano.
""")