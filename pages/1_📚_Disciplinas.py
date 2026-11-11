import os
from pathlib import Path
import streamlit as st
import requests

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")

def load_env():
    """Carrega as variáveis do arquivo .env localizado na raiz do projeto como fallback."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key:
                        os.environ[key] = val

def get_config(key: str, default: str = "") -> str:
    """Obtém configuração prioritariamente de st.secrets, com fallback para os.environ."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).rstrip("/")
    except Exception:
        pass
    return os.environ.get(key, default).rstrip("/")

load_env()
BASE_URL = (
    get_config("XANO_SUBJECTS_BASE_URL")
    or get_config("XANO_API_BASE_URL")
    or get_config("XANO_AUTH_BASE_URL")
    or st.session_state.get("xano_api_base_url", "")
).rstrip("/")

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
    """Busca as disciplinas da tabela subjects do Xano com autenticação."""
    if not BASE_URL:
        return st.session_state.get("cached_subjects", [])
    
    if not token:
        return st.session_state.get("cached_subjects", [])
    
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/subjects", headers=headers, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                st.session_state["cached_subjects"] = data
                return data
        elif response.status_code in [401, 403]:
            st.warning("Sessão expirada ou não autenticada. Faça login na página de Perfil.")
        else:
            st.error(f"Erro ao consultar disciplinas no Xano (Status {response.status_code}).")
    except requests.exceptions.RequestException as e:
        st.warning(f"Falha de conexão com o Xano: {e}. Exibindo dados locais.")
    
    return st.session_state.get("cached_subjects", [])

def add_subject(name, teacher, hours):
    """Envia uma nova disciplina para o endpoint POST /subjects do Xano."""
    payload = {
        "name": name.strip(),
        "teacher": teacher.strip() if teacher else "",
        "hours": int(hours) if hours else 0
    }

    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.post(f"{BASE_URL}/subjects", json=payload, headers=headers, timeout=8)
            if response.status_code in [200, 201]:
                new_record = response.json()
                if isinstance(new_record, dict) and "id" in new_record:
                    st.session_state["cached_subjects"].append(new_record)
                return True, "Disciplina cadastrada com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão expirada ou não autenticada. Faça login na página de Perfil."
            else:
                return False, f"Erro do Xano ({response.status_code}): {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão com o Xano: {e}"
    elif BASE_URL and not token:
        return False, "Você precisa fazer login na aba Perfil para salvar a disciplina no Xano."
    else:
        # Fallback local quando BASE_URL não configurada
        fallback_record = {"id": len(st.session_state["cached_subjects"]) + 1, **payload}
        st.session_state["cached_subjects"].append(fallback_record)
        return True, "Disciplina cadastrada no cache local (configure XANO_API_BASE_URL no .env)."

def update_subject(subject_id, name, teacher, hours):
    """Atualiza uma disciplina através do endpoint PATCH /subjects/{id} no Xano."""
    payload = {
        "name": name.strip(),
        "teacher": teacher.strip() if teacher else "",
        "hours": int(hours) if hours else 0
    }

    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.patch(f"{BASE_URL}/subjects/{subject_id}", json=payload, headers=headers, timeout=8)
            if response.status_code == 200:
                for s in st.session_state["cached_subjects"]:
                    if s.get("id") == subject_id:
                        s.update(payload)
                        break
                return True, "Disciplina atualizada com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão expirada ou não autenticada."
            else:
                return False, f"Erro ao atualizar no Xano ({response.status_code}): {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão ao atualizar: {e}"
    else:
        for s in st.session_state["cached_subjects"]:
            if s.get("id") == subject_id:
                s.update(payload)
                break
        return True, "Disciplina atualizada localmente."

def remove_subject(subject_id):
    """Exclui uma disciplina no backend Xano via DELETE /subjects/{id}."""
    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{BASE_URL}/subjects/{subject_id}", headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                st.session_state["cached_subjects"] = [s for s in st.session_state["cached_subjects"] if s.get("id") != subject_id]
                return True, "Disciplina excluída com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada ou registro pertencente a outro usuário."
            else:
                return False, f"Erro ao excluir no Xano ({response.status_code})."
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão ao excluir: {e}"

    st.session_state["cached_subjects"] = [s for s in st.session_state["cached_subjects"] if s.get("id") != subject_id]
    return True, "Disciplina removida do cache local."

# Cabeçalho da Página
st.title("📚 Gestão de Disciplinas")

# Barra de status de conexão do usuário
if user and token:
    st.caption(f"👤 Usuário conectado: **{user.get('name', 'Estudante')}** ({user.get('email', '')}) — Sincronizado com Xano")
elif BASE_URL and not token:
    st.warning("⚠️ Você não está autenticado. Acesse a página **👤 Perfil** para fazer login e persistir dados no Xano.")
else:
    st.info("💡 **Dica:** Acesse a aba **👤 Perfil** para configurar e conectar sua conta ao Xano.")

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
                        ok, msg = remove_subject(s_id)
                        if ok:
                            st.toast(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                
                # Expander para edição (PATCH /subjects/{id})
                with st.expander(f"✏️ Editar {s_name}", expanded=False):
                    with st.form(f"form_edit_subj_{s_id}"):
                        edit_name = st.text_input("Nome da Disciplina", value=s_name)
                        edit_teacher = st.text_input("Professor", value=s_teacher if s_teacher != "Não informado" else "")
                        edit_hours = st.number_input("Carga Horária", min_value=0, max_value=500, value=int(s_hours), step=10)
                        
                        btn_salvar_edicao = st.form_submit_button("Atualizar no Xano")
                        if btn_salvar_edicao:
                            if not edit_name.strip():
                                st.error("O nome da disciplina não pode ser vazio.")
                            else:
                                ok, msg = update_subject(s_id, edit_name, edit_teacher, edit_hours)
                                if ok:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
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
