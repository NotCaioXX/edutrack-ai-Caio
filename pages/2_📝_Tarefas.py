import os
import sys
from pathlib import Path
from datetime import date, datetime
import streamlit as st
import requests

# Setup project path for components import
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.navbar import render_navbar, render_page_header, require_auth

page_icon_path = PROJECT_ROOT / "assets" / "logos" / "tarefa_00000.png"
st.set_page_config(
    page_title="Tarefas",
    page_icon=str(page_icon_path) if page_icon_path.exists() else None,
    layout="wide"
)
render_navbar()
require_auth()

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
    get_config("XANO_TASKS_BASE_URL")
    or get_config("XANO_API_BASE_URL")
    or get_config("XANO_AUTH_BASE_URL")
    or st.session_state.get("xano_api_base_url", "")
).rstrip("/")

SUBJECTS_BASE_URL = (
    get_config("XANO_SUBJECTS_BASE_URL")
    or get_config("XANO_API_BASE_URL")
    or get_config("XANO_AUTH_BASE_URL")
    or st.session_state.get("xano_api_base_url", "")
).rstrip("/")

STATUS_OPTIONS = ["pending", "in_progress", "completed"]
STATUS_LABELS = {
    "pending": "Pendente",
    "in_progress": "Em progresso",
    "completed": "Concluído"
}

def format_status(st_code: str) -> str:
    return STATUS_LABELS.get(st_code, st_code)

# Inicialização de estado de sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "cached_tasks" not in st.session_state:
    st.session_state["cached_tasks"] = []
if "cached_subjects" not in st.session_state:
    st.session_state["cached_subjects"] = []

token = st.session_state.get("auth_token")
user = st.session_state.get("user_info")
user_id = user.get("id") if user else None

def get_auth_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}

def fetch_subjects():
    """Busca as disciplinas disponíveis no Xano com autenticação."""
    target_url = SUBJECTS_BASE_URL or BASE_URL
    if not target_url or not token:
        return st.session_state.get("cached_subjects", [])
    try:
        headers = get_auth_headers()
        response = requests.get(f"{target_url}/subjects", headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                st.session_state["cached_subjects"] = data
                return data
    except requests.exceptions.RequestException:
        pass
    return st.session_state.get("cached_subjects", [])

def fetch_tasks():
    """Busca as tarefas da tabela academic_tasks do Xano com autenticação."""
    if not BASE_URL:
        return st.session_state.get("cached_tasks", [])
    
    if not token:
        return st.session_state.get("cached_tasks", [])
    
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/academic_tasks", headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                st.session_state["cached_tasks"] = data
                return data
        elif response.status_code in [401, 403]:
            st.warning("Sessão expirada ou não autenticada. Faça login na página de Perfil.")
        else:
            try:
                err_detail = response.json().get("message") or response.json()
            except Exception:
                err_detail = response.text
            st.error(f"Erro ao consultar tarefas no Xano (Status {response.status_code}): {err_detail}")
    except requests.exceptions.RequestException as e:
        st.warning(f"Falha de conexão com o Xano: {e}. Exibindo dados locais.")
    
    return st.session_state.get("cached_tasks", [])

def add_task(title, description, due_date_val, status_val, subject_id, grade_val=None):
    """Envia uma nova tarefa para a tabela academic_tasks do Xano via POST."""
    payload = {
        "subject_id": int(subject_id) if subject_id else 0,
        "title": title.strip(),
        "description": description.strip() if description else "",
        "due_date": due_date_val.strftime("%Y-%m-%d") if due_date_val else None,
        "status": status_val or "pending",
        "grade": float(grade_val) if grade_val is not None else None
    }

    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.post(f"{BASE_URL}/academic_tasks", json=payload, headers=headers, timeout=8)
            if response.status_code in [200, 201]:
                new_task = response.json()
                if isinstance(new_task, dict) and "id" in new_task:
                    st.session_state["cached_tasks"].append(new_task)
                return True, "Tarefa cadastrada com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada. Faça login na página de Perfil."
            else:
                return False, f"Erro do Xano ({response.status_code}): {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão com o Xano: {e}"
    elif BASE_URL and not token:
        return False, "Você precisa fazer login na aba Perfil para persistir a tarefa no Xano."
    else:
        fallback_task = {"id": len(st.session_state["cached_tasks"]) + 1, **payload}
        st.session_state["cached_tasks"].append(fallback_task)
        return True, "Tarefa cadastrada no cache local (configure XANO_API_BASE_URL no .env)."

def update_task_status(task_id, new_status):
    """Atualiza o status de uma tarefa no Xano via PATCH /academic_tasks/{id}."""
    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.patch(f"{BASE_URL}/academic_tasks/{task_id}", json={"status": new_status}, headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                for t in st.session_state["cached_tasks"]:
                    if t.get("id") == task_id:
                        t["status"] = new_status
                        break
                return True, "Status atualizado no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada para atualizar esta tarefa."
            else:
                return False, f"Erro do Xano ({response.status_code})."
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {e}"

    for t in st.session_state["cached_tasks"]:
        if t.get("id") == task_id:
            t["status"] = new_status
            break
    return True, "Status atualizado localmente."

def update_task_grade(task_id, grade_val):
    """Atualiza exclusivamente a nota de uma tarefa no Xano via PATCH /academic_tasks/{id}."""
    payload = {"grade": float(grade_val) if grade_val is not None else None}
    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.patch(f"{BASE_URL}/academic_tasks/{task_id}", json=payload, headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                for t in st.session_state["cached_tasks"]:
                    if t.get("id") == task_id:
                        t["grade"] = payload["grade"]
                        break
                return True, "Nota atualizada com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada para atualizar a nota desta tarefa."
            else:
                return False, f"Erro do Xano ({response.status_code})."
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão ao salvar nota: {e}"

    for t in st.session_state["cached_tasks"]:
        if t.get("id") == task_id:
            t["grade"] = payload["grade"]
            break
    return True, "Nota salva localmente."

def update_task_details(task_id, title, description, due_date_val, status_val, subject_id, grade_val=None):
    """Atualiza todos os dados de uma tarefa no Xano via PATCH /academic_tasks/{id}."""
    payload = {
        "subject_id": int(subject_id) if subject_id else 0,
        "title": title.strip(),
        "description": description.strip() if description else "",
        "due_date": due_date_val.strftime("%Y-%m-%d") if due_date_val else None,
        "status": status_val,
        "grade": float(grade_val) if grade_val is not None else None
    }

    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.patch(f"{BASE_URL}/academic_tasks/{task_id}", json=payload, headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                for t in st.session_state["cached_tasks"]:
                    if t.get("id") == task_id:
                        t.update(payload)
                        break
                return True, "Tarefa atualizada com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada ou registro pertencente a outro usuário."
            else:
                return False, f"Erro do Xano ({response.status_code}): {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão ao atualizar tarefa: {e}"
    else:
        for t in st.session_state["cached_tasks"]:
            if t.get("id") == task_id:
                t.update(payload)
                break
        return True, "Tarefa atualizada localmente."

def remove_task(task_id):
    """Exclui uma tarefa no Xano via DELETE /academic_tasks/{id}."""
    if BASE_URL and token:
        try:
            headers = get_auth_headers()
            response = requests.delete(f"{BASE_URL}/academic_tasks/{task_id}", headers=headers, timeout=8)
            if response.status_code in [200, 204]:
                st.session_state["cached_tasks"] = [t for t in st.session_state["cached_tasks"] if t.get("id") != task_id]
                return True, "Tarefa excluída com sucesso no Xano!"
            elif response.status_code in [401, 403]:
                return False, "Sessão não autorizada ou tarefa pertencente a outro usuário."
            else:
                return False, f"Erro ao excluir tarefa no Xano ({response.status_code})."
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão ao excluir tarefa: {e}"

    st.session_state["cached_tasks"] = [t for t in st.session_state["cached_tasks"] if t.get("id") != task_id]
    return True, "Tarefa removida do cache local."

# Cabeçalho da Página
render_page_header("Gestão de Tarefas Acadêmicas", "tarefa_00000.png")

if user and token:
    st.caption(f"Usuário conectado: **{user.get('name', 'Estudante')}** ({user.get('email', '')}) — Sincronizado com Xano")
elif BASE_URL and not token:
    st.warning("Você não está autenticado. Acesse a página **Perfil** para fazer login e sincronizar tarefas com o Xano.")
else:
    st.info("**Dica:** Acesse a aba **Perfil** para fazer login e associar suas tarefas à sua conta no Xano.")

# Carrega matérias para vincular as tarefas
subjects = fetch_subjects()
subject_map = {s.get("id"): s.get("name") for s in subjects if s.get("id")}

tab_lista, tab_novo = st.tabs(["Minhas Tarefas", "Nova Tarefa"])

# Aba 1: Listagem e Filtros
with tab_lista:
    tasks = fetch_tasks()
    
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        busca = st.text_input("Buscar tarefa...", placeholder="Ex: Trabalho de Banco de Dados").strip().lower()
    with col_f2:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            ["Todos", "pending", "in_progress", "completed"],
            format_func=lambda s: "Todos" if s == "Todos" else STATUS_LABELS.get(s, s)
        )
    with col_f3:
        opcoes_disc = ["Todas"] + [f"{s.get('name')} (ID: {s.get('id')})" for s in subjects]
        filtro_disc = st.selectbox("Filtrar por Disciplina", opcoes_disc)

    # Filtragem
    filtered_tasks = tasks
    if busca:
        filtered_tasks = [t for t in filtered_tasks if busca in (t.get("title") or "").lower() or busca in (t.get("description") or "").lower()]
    if filtro_status != "Todos":
        filtered_tasks = [t for t in filtered_tasks if t.get("status") == filtro_status]
    if filtro_disc != "Todas":
        selected_id = int(filtro_disc.split("ID: ")[1].rstrip(")"))
        filtered_tasks = [t for t in filtered_tasks if t.get("subject_id") == selected_id]

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total de Tarefas", len(tasks))
    pendentes = sum(1 for t in tasks if t.get("status") != "completed")
    col_m2.metric("Pendentes / Em Andamento", pendentes)
    concluidas = sum(1 for t in tasks if t.get("status") == "completed")
    col_m3.metric("Concluídas", concluidas)

    st.markdown("---")

    if not filtered_tasks:
        st.info("Nenhuma tarefa encontrada com os filtros selecionados. Crie uma na aba **Nova Tarefa**.")
    else:
        for t in filtered_tasks:
            t_id = t.get("id")
            t_title = t.get("title", "Sem Título")
            t_desc = t.get("description", "")
            t_due = t.get("due_date", "Sem prazo")
            t_status = t.get("status", "pending")
            t_subj_id = t.get("subject_id")
            t_subj_name = subject_map.get(t_subj_id, f"Disciplina #{t_subj_id}" if t_subj_id else "Geral")
            t_grade = t.get("grade")

            if t_status == "completed":
                if t_grade is not None and t_grade != "":
                    grade_label = f"Nota: {float(t_grade):.1f}"
                else:
                    grade_label = "Nota: pendente"
                header_title = f"{t_title} — {t_subj_name} (Prazo: {t_due}) • {grade_label}"
            else:
                header_title = f"{t_title} — {t_subj_name} (Prazo: {t_due})"

            with st.expander(header_title, expanded=(t_status != "completed")):
                st.write(f"**Descrição:** {t_desc if t_desc else 'Nenhuma observação adicionada.'}")
                
                c_act1, c_act2, c_act3 = st.columns([1.5, 1.8, 1])
                with c_act1:
                    novo_st = st.selectbox(
                        "Alterar Status Rápido", 
                        STATUS_OPTIONS, 
                        index=STATUS_OPTIONS.index(t_status) if t_status in STATUS_OPTIONS else 0,
                        format_func=format_status,
                        key=f"status_sel_{t_id}"
                    )
                    if novo_st != t_status:
                        ok, msg = update_task_status(t_id, novo_st)
                        if ok:
                            st.toast(msg)
                            st.rerun()
                        else:
                            st.error(msg)

                with c_act2:
                    if t_status == "completed":
                        curr_g = float(t_grade) if (t_grade is not None and t_grade != "") else 0.0
                        col_g_val, col_g_btn = st.columns([1.2, 1])
                        with col_g_val:
                            nova_nota = st.number_input(
                                "Nota (0.0 a 10.0)",
                                min_value=0.0,
                                max_value=10.0,
                                value=curr_g,
                                step=0.1,
                                format="%.1f",
                                key=f"grade_input_{t_id}"
                            )
                        with col_g_btn:
                            st.write("")
                            st.write("")
                            if st.button("Salvar Nota", key=f"btn_save_grade_{t_id}", use_container_width=True):
                                ok, msg = update_task_grade(t_id, nova_nota)
                                if ok:
                                    st.toast(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)

                with c_act3:
                    st.write("")
                    st.write("")
                    if st.button("Excluir", key=f"del_task_{t_id}", help="Excluir tarefa no Xano", use_container_width=True):
                        ok, msg = remove_task(t_id)
                        if ok:
                            st.toast(msg)
                            st.rerun()
                        else:
                            st.error(msg)

                # Formulário de Edição Detalhada (PATCH /academic_tasks/{id})
                with st.expander("Editar detalhes da tarefa", expanded=False):
                    with st.form(f"form_edit_task_{t_id}"):
                        edit_titulo = st.text_input("Título", value=t_title)
                        
                        # Data de entrega
                        parsed_date = date.today()
                        if t_due and t_due != "Sem prazo":
                            try:
                                parsed_date = datetime.strptime(str(t_due)[:10], "%Y-%m-%d").date()
                            except ValueError:
                                pass
                        edit_due = st.date_input("Prazo", value=parsed_date, key=f"edit_due_{t_id}")
                        
                        # Seleção da disciplina
                        current_subj_idx = 0
                        disc_options = [f"{s.get('name')} (ID: {s.get('id')})" for s in subjects]
                        for idx, s in enumerate(subjects):
                            if s.get("id") == t_subj_id:
                                current_subj_idx = idx
                                break
                        edit_disc = st.selectbox(
                            "Disciplina Vinculada",
                            options=disc_options if disc_options else ["Nenhuma disciplina disponível"],
                            index=current_subj_idx if disc_options else 0,
                            key=f"edit_disc_{t_id}"
                        )
                        edit_disc_id = int(edit_disc.split("ID: ")[1].rstrip(")")) if (disc_options and "ID: " in edit_disc) else (t_subj_id or 1)

                        edit_desc = st.text_area("Descrição", value=t_desc)
                        
                        col_edit_st, col_edit_gr = st.columns(2)
                        with col_edit_st:
                            edit_status = st.selectbox(
                                "Status", 
                                STATUS_OPTIONS, 
                                index=STATUS_OPTIONS.index(t_status) if t_status in STATUS_OPTIONS else 0, 
                                format_func=format_status,
                                key=f"edit_st_{t_id}"
                            )
                        with col_edit_gr:
                            curr_grade = float(t_grade) if (t_grade is not None and t_grade != "") else 0.0
                            edit_grade = st.number_input(
                                "Nota da Atividade (0.0 a 10.0)",
                                min_value=0.0,
                                max_value=10.0,
                                value=curr_grade,
                                step=0.1,
                                format="%.1f",
                                key=f"edit_grade_{t_id}"
                            )

                        btn_edit = st.form_submit_button("Atualizar Tarefa no Xano")
                        if btn_edit:
                            if not edit_titulo.strip():
                                st.error("O título não pode ser vazio.")
                            else:
                                ok, msg = update_task_details(t_id, edit_titulo, edit_desc, edit_due, edit_status, edit_disc_id, edit_grade)
                                if ok:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)

# Aba 2: Cadastro de Nova Tarefa
with tab_novo:
    st.subheader("Cadastrar Nova Tarefa")
    
    with st.form("form_task"):
        titulo = st.text_input("Título da Tarefa *", placeholder="Ex: Lista 3 de Exercícios")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            if subjects:
                disciplina_escolhida = st.selectbox(
                    "Disciplina Vinculada *",
                    options=[f"{s.get('name')} (ID: {s.get('id')})" for s in subjects]
                )
                subj_id_selected = int(disciplina_escolhida.split("ID: ")[1].rstrip(")"))
            else:
                st.warning("Nenhuma disciplina encontrada. Você pode cadastrar uma disciplina primeiro na aba Disciplinas.")
                subj_id_selected = st.number_input("ID da Disciplina", min_value=1, value=1)
        
        with col_form2:
            prazo = st.date_input("Data de Entrega / Prazo", value=date.today())
        
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            status_inicial = st.selectbox(
                "Status Inicial", 
                STATUS_OPTIONS,
                format_func=format_status
            )
        with col_st2:
            nota_inicial = st.number_input(
                "Nota Inicial (se concluída)",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                format="%.1f"
            )
        descricao = st.text_area("Descrição / Orientações", placeholder="Detalhes, capítulos a ler, links ou requisitos da entrega.")

        submitted = st.form_submit_button("Salvar Tarefa no Xano", use_container_width=True)
        if submitted:
            if not titulo.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                grade_to_save = nota_inicial if status_inicial == "completed" else None
                success, msg = add_task(titulo, descricao, prazo, status_inicial, subj_id_selected, grade_to_save)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
