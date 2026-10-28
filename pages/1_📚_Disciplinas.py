import os
from pathlib import Path
import streamlit as st
import requests

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")

def load_env():
    """Carrega as variáveis do arquivo .env localizado na raiz do projeto."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
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

# Inicialização de estado de sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "cached_subjects" not in st.session_state:
    st.session_state["cached_subjects"] = []

token = st.session_state.get("auth_token")
user = st.session_state.get("user_info")
user_id = user.get("id") if user else None

def get_auth_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}

def fetch_subjects():
    """Busca as disciplinas da tabela subjects do Xano."""
    if not BASE_URL:
        return st.session_state.get("cached_subjects", [])
    
    try:
        headers = get_auth_headers()
        params = {"user_id": user_id} if user_id else {}
        response = requests.get(f"{BASE_URL}/subjects", headers=headers, params=params, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                st.session_state["cached_subjects"] = data
                return data
        elif response.status_code == 401:
            st.warning("Sessão expirada ou não autenticada. Faça login na página de Perfil.")
    except requests.exceptions.RequestException:
        pass # Mantém dados em cache se houver falha de rede
    
    return st.session_state.get("cached_subjects", [])

def add_subject(name, teacher, hours):
    """Envia uma nova disciplina para o backend Xano."""
    payload = {
        "name": name.strip(),
        "teacher": teacher.strip() if teacher else "",
        "hours": int(hours) if hours else 0,
        "user_id": user_id or 1
    }

    if BASE_URL:
        try:
            headers = get_auth_headers()
            response = requests.post(f"{BASE_URL}/subjects", json=payload, headers=headers, timeout=8)
            if response.status_code in [200, 201]:
                return True, "Disciplina cadastrada com sucesso no Xano!"
            else:
                # Se o endpoint ainda não estiver ativo no Xano, salva localmente para demonstração
                fallback_record = {"id": len(st.session_state["cached_subjects"]) + 1, **payload}
                st.session_state["cached_subjects"].append(fallback_record)
                return True, f"Disciplina salva localmente (API retornou status {response.status_code})."
        except requests.exceptions.RequestException as e:
            fallback_record = {"id": len(st.session_state["cached_subjects"]) + 1, **payload}
            st.session_state["cached_subjects"].append(fallback_record)
            return True, f"Disciplina salva no cache local (Erro de conexão: {e})."
    else:
        fallback_record = {"id": len(st.session_state["cached_subjects"]) + 1, **payload}
        st.session_state["cached_subjects"].append(fallback_record)
        return True, "Disciplina cadastrada no cache local (configure XANO_API_BASE_URL no .env)."

def remove_subject(subject_id):
    """Exclui uma disciplina no backend Xano ou cache local."""
    if BASE_URL:
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{BASE_URL}/subjects/{subject_id}", headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                st.session_state["cached_subjects"] = [s for s in st.session_state["cached_subjects"] if s.get("id") != subject_id]
                return True
        except requests.exceptions.RequestException:
            pass

    st.session_state["cached_subjects"] = [s for s in st.session_state["cached_subjects"] if s.get("id") != subject_id]
    return True

# Cabeçalho da Página
st.title("📚 Gestão de Disciplinas")

# Barra de status de conexão do usuário
if user:
    st.caption(f"👤 Usuário conectado: **{user.get('name', 'Estudante')}** ({user.get('email', '')})")
else:
    st.info("💡 **Dica:** Você está navegando como visitante. Acesse a aba **👤 Perfil** para fazer login e associar disciplinas à sua conta.")

tab_lista, tab_novo = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

# Aba 1: Listagem
with tab_lista:
    subjects = fetch_subjects()
    
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric("Total de Disciplinas", len(subjects))
    total_hours = sum(s.get("hours", 0) or 0 for s in subjects)
    col_metric2.metric("Carga Horária Total", f"{total_hours}h")
    
    st.markdown("---")
    
    if not subjects:
        st.info("Nenhuma disciplina cadastrada ainda. Utilize a aba **➕ Nova Disciplina** para cadastrar a sua primeira matéria.")
    else:
        for subj in subjects:
            s_id = subj.get("id")
            s_name = subj.get("name", "Sem Nome")
            s_teacher = subj.get("teacher") or "Não informado"
            s_hours = subj.get("hours") or 0
            
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
                c1.markdown(f"**📖 {s_name}**")
                c2.write(f"👨‍🏫 Prof: {s_teacher}")
                c3.write(f"⏱️ {s_hours} horas")
                with c4:
                    if st.button("🗑️", key=f"del_subj_{s_id}", help="Excluir disciplina"):
                        remove_subject(s_id)
                        st.toast(f"Disciplina '{s_name}' excluída.")
                        st.rerun()
                st.divider()

# Aba 2: Cadastro
with tab_novo:
    st.subheader("Cadastrar Nova Disciplina na Tabela `subjects`")
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Algoritmos e Estruturas de Dados")
        professor = st.text_input("Professor / Instrutor", placeholder="Ex: Dr. Carlos Silva")
        carga_horaria = st.number_input("Carga Horária (Horas)", min_value=0, max_value=500, value=60, step=10)
        
        submitted = st.form_submit_button("Salvar Disciplina", use_container_width=True)
        if submitted:
            if not nome.strip():
                st.error("O nome da disciplina é obrigatório.")
            else:
                success, msg = add_subject(nome, professor, carga_horaria)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
