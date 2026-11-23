import os
import calendar
from datetime import date, datetime
from pathlib import Path
import streamlit as st
import requests

from components.navbar import render_navbar, render_section_header

page_icon_path = Path(__file__).resolve().parent / "assets" / "logos" / "logo_00000.png"
st.set_page_config(
    page_title="EduTrack AI",
    page_icon=str(page_icon_path) if page_icon_path.exists() else None,
    layout="wide"
)
render_navbar()

def load_env():
    """Carrega as variáveis do arquivo .env localizado na raiz do projeto como fallback."""
    env_path = Path(__file__).resolve().parent / ".env"
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
SUBJECTS_URL = (get_config("XANO_SUBJECTS_BASE_URL") or get_config("XANO_API_BASE_URL") or get_config("XANO_AUTH_BASE_URL", "")).rstrip("/")
TASKS_URL = (get_config("XANO_TASKS_BASE_URL") or get_config("XANO_API_BASE_URL") or get_config("XANO_AUTH_BASE_URL", "")).rstrip("/")

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

# ==============================================================================
# FLUXO 1: USUÁRIO NÃO LOGADO (VISITANTE)
# ==============================================================================
if not token:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; padding: 36px 32px; border: 1px solid #334155; margin-bottom: 28px;">
            <h1 style="color: #f8fafc; font-size: 2.3rem; margin-top: 0; margin-bottom: 12px; font-weight: 700;">
                Bem-vindo ao EduTrack AI
            </h1>
            <p style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.6; max-width: 820px; margin-bottom: 24px;">
                Sua plataforma completa de gestão acadêmica inteligente. Organize suas disciplinas, acompanhe prazos de tarefas com calendário visual, calcule médias ponderadas e conte com um tutor de inteligência artificial dedicado aos seus estudos.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_card1, col_card2, col_card3 = st.columns(3)

    with col_card1:
        with st.container(border=True):
            st.markdown("### Gestão de Matérias")
            st.write("Cadastre suas disciplinas com professor e carga horária. Tenha controle do progresso de cada matéria em tempo real.")

    with col_card2:
        with st.container(border=True):
            st.markdown("### Prazos e Calendário")
            st.write("Adicione atividades com datas de entrega e acompanhe o calendário dinâmico com marcadores visuais para não perder prazos.")

    with col_card3:
        with st.container(border=True):
            st.markdown("### Tutor IA de Estudos")
            st.write("Converse com um mentor inteligente sobre métodos como Feynman, Pomodoro e receba orientações com base nas suas notas.")

    st.write("")
    st.info("Para acessar as disciplinas, tarefas, relatórios em PDF e o Tutor IA, entre com sua conta ou crie um novo cadastro gratuito.")

    col_act1, col_act2, _ = st.columns([1.6, 1.6, 3.2])
    with col_act1:
        st.page_link("pages/4_👤_Perfil.py", label="Entrar na Minha Conta", use_container_width=True)
    with col_act2:
        st.page_link("pages/4_👤_Perfil.py", label="Criar Nova Conta", use_container_width=True)

    st.stop()

# ==============================================================================
# FLUXO 2: USUÁRIO LOGADO
# ==============================================================================
def get_auth_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}

def sync_dashboard_metrics():
    """Sincroniza contagens e dados do Xano com tratamento resiliente."""
    subjects_count = len(st.session_state.get("cached_subjects", []))
    tasks_pending_count = sum(1 for t in st.session_state.get("cached_tasks", []) if t.get("status") != "completed")

    if SUBJECTS_URL:
        try:
            headers = get_auth_headers()
            resp_subj = requests.get(f"{SUBJECTS_URL}/subjects", headers=headers, timeout=5)
            if resp_subj.status_code == 200 and isinstance(resp_subj.json(), list):
                st.session_state["cached_subjects"] = resp_subj.json()
                subjects_count = len(resp_subj.json())
        except requests.exceptions.RequestException:
            pass

    if TASKS_URL:
        try:
            headers = get_auth_headers()
            resp_tasks = requests.get(f"{TASKS_URL}/academic_tasks", headers=headers, timeout=5)
            if resp_tasks.status_code == 200 and isinstance(resp_tasks.json(), list):
                st.session_state["cached_tasks"] = resp_tasks.json()
                tasks_pending_count = sum(1 for t in resp_tasks.json() if t.get("status") != "completed")
        except requests.exceptions.RequestException:
            pass

    return subjects_count, tasks_pending_count

subj_count, pending_count = sync_dashboard_metrics()

# Mensagem de Boas-Vindas ao usuário autenticado
student_name = user.get("name", "Estudante") if user else "Estudante"
st.markdown(f"### Olá, **{student_name}**!")
st.caption("Acompanhe o resumo do seu semestre acadêmico:")

# Se usuário não tem matérias nem tarefas cadastradas, exibe card de onboarding
if subj_count == 0:
    st.markdown(
        """
        <div style="background-color: #172554; border: 1px solid #1d4ed8; border-radius: 12px; padding: 22px; margin-top: 10px; margin-bottom: 24px;">
            <h3 style="color: #93c5fd; margin-top: 0; margin-bottom: 8px;">Primeiros Passos no EduTrack AI</h3>
            <p style="color: #e0f2fe; margin-bottom: 14px; font-size: 1.05rem;">
                Você ainda não possui disciplinas cadastradas. Comece adicionando suas matérias do semestre para desbloquear o calendário de entregas, o acompanhamento de progresso e as análises do Tutor IA!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col_ob1, col_ob2, _ = st.columns([1.8, 1.8, 3.0])
    with col_ob1:
        st.page_link("pages/1_📚_Disciplinas.py", label="Cadastrar Primeira Matéria", use_container_width=True)
    with col_ob2:
        st.page_link("pages/2_📝_Tarefas.py", label="Cadastrar Primeira Tarefa", use_container_width=True)
    st.markdown("---")

# Métricas Visuais Dinâmicas
col1, col2 = st.columns(2)
col1.metric("Disciplinas Cadastradas", str(subj_count))
col2.metric("Tarefas Pendentes", str(pending_count))

st.markdown("---")

# Funções auxiliares para Calendário e Progresso
def parse_task_date(date_val):
    if not date_val:
        return None
    if isinstance(date_val, (date, datetime)):
        return date_val if isinstance(date_val, date) else date_val.date()
    if isinstance(date_val, str):
        date_str = date_val.split("T")[0].strip()
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return None
    return None

cached_subjects = st.session_state.get("cached_subjects", [])
cached_tasks = st.session_state.get("cached_tasks", [])
subject_map = {s.get("id"): s.get("name", f"Disciplina {s.get('id')}") for s in cached_subjects if s.get("id")}

# Layout Principal em duas colunas:
# - Coluna Esquerda: Quadro de informações de visão geral de progresso em cada matéria que não está completa
# - Coluna Direita: Calendário com próximas datas de entregas de atividades e lista de matérias associadas
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    render_section_header("Visão Geral de Progresso (Matérias Incompletas)", "prog_00000.png")
    st.write("Acompanhe o andamento das matérias que ainda não atingiram 100% de conclusão:")

    incomplete_subjects = []
    for subj in cached_subjects:
        s_id = subj.get("id")
        s_name = subj.get("name", "Sem Nome")
        subj_tasks = [t for t in cached_tasks if t.get("subject_id") == s_id]
        total_t = len(subj_tasks)
        completed_t = sum(1 for t in subj_tasks if t.get("status") == "completed")
        pct = round((completed_t / total_t * 100), 1) if total_t > 0 else 0.0
        
        if pct < 100.0 or total_t == 0:
            incomplete_subjects.append({
                "id": s_id,
                "name": s_name,
                "teacher": subj.get("teacher"),
                "hours": subj.get("hours"),
                "total_tasks": total_t,
                "completed_tasks": completed_t,
                "percentage": pct
            })

    if not cached_subjects:
        st.info("Nenhuma disciplina cadastrada no momento. Acesse a página **Disciplinas** para adicionar suas matérias.")
    elif not incomplete_subjects:
        st.success("Parabéns! Todas as suas matérias cadastradas estão 100% concluídas.")
    else:
        for item in incomplete_subjects:
            with st.container(border=True):
                sub_c1, sub_c2 = st.columns([3, 1])
                sub_c1.markdown(f"**{item['name']}**")
                sub_c2.markdown(f"**{item['percentage']}%**")
                
                prog_frac = min(max(item["percentage"] / 100.0, 0.0), 1.0)
                st.progress(prog_frac)
                
                details = f"{item['completed_tasks']} de {item['total_tasks']} tarefas concluídas"
                if item.get("teacher"):
                    details += f" • Prof(a): {item['teacher']}"
                st.caption(details)

with col_right:
    st.subheader("Calendário de Próximas Entregas")
    
    today = datetime.now().date()
    curr_year = today.year
    curr_month = today.month
    
    # Nomes dos meses em português
    month_names_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    month_title = f"{month_names_pt.get(curr_month, 'Mês')} {curr_year}"
    
    # Identificar tarefas com data no mês atual ou futuras
    tasks_with_dates = []
    days_with_pending = set()
    days_with_completed = set()
    
    for t in cached_tasks:
        d = parse_task_date(t.get("due_date"))
        if d:
            tasks_with_dates.append({**t, "parsed_due_date": d})
            if d.year == curr_year and d.month == curr_month:
                if t.get("status") != "completed":
                    days_with_pending.add(d.day)
                else:
                    days_with_completed.add(d.day)
    
    # Construir HTML do calendário
    cal_matrix = calendar.monthcalendar(curr_year, curr_month)
    
    rows_html = ""
    for week in cal_matrix:
        cells_html = ""
        for day in week:
            if day == 0:
                cells_html += '<td style="padding: 8px 4px; color: #475569;">-</td>'
            else:
                has_pending = day in days_with_pending
                is_today = (day == today.day and curr_month == today.month and curr_year == today.year)
                
                if has_pending and is_today:
                    # Tarefa pendente em dia atual: círculo vermelho com contorno azul
                    cells_html += (
                        f'<td style="padding: 6px 2px; text-align: center;">'
                        f'<span style="display: inline-block; width: 28px; height: 28px; line-height: 24px; '
                        f'border-radius: 50%; background-color: #ff0000; border: 2px solid #2563eb; color: #ffffff; font-weight: bold; font-size: 13px;">'
                        f'{day}</span></td>'
                    )
                elif has_pending:
                    # Tarefas pendentes: círculo preenchido em vermelho #ff0000
                    cells_html += (
                        f'<td style="padding: 6px 2px; text-align: center;">'
                        f'<span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; '
                        f'border-radius: 50%; background-color: #ff0000; color: #ffffff; font-weight: bold; font-size: 13px;">'
                        f'{day}</span></td>'
                    )
                elif is_today:
                    # Dia de hoje: círculo preenchido em azul #2563eb
                    cells_html += (
                        f'<td style="padding: 6px 2px; text-align: center;">'
                        f'<span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; '
                        f'border-radius: 50%; background-color: #2563eb; color: #ffffff; font-weight: bold; font-size: 13px;">'
                        f'{day}</span></td>'
                    )
                elif day in days_with_completed:
                    # Tarefas concluídas: círculo com borda verde
                    cells_html += (
                        f'<td style="padding: 6px 2px; text-align: center;">'
                        f'<span style="display: inline-block; width: 28px; height: 28px; line-height: 26px; '
                        f'border-radius: 50%; border: 1px solid #10b981; color: #10b981; font-weight: bold; font-size: 13px;">'
                        f'{day}</span></td>'
                    )
                else:
                    cells_html += f'<td style="padding: 8px 4px; text-align: center; color: #e2e8f0; font-size: 13px;">{day}</td>'
        rows_html += f"<tr>{cells_html}</tr>"
        
    calendar_html = f"""
    <div style="background-color: #1e1e1e; border-radius: 12px; padding: 14px; border: 1px solid #333333; margin-bottom: 18px;">
        <div style="font-weight: 700; font-size: 16px; margin-bottom: 10px; text-align: center; color: #f1f5f9;">
            {month_title}
        </div>
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead>
                <tr style="color: #94a3b8; font-size: 12px; font-weight: 600;">
                    <th style="padding: 4px;">Seg</th>
                    <th style="padding: 4px;">Ter</th>
                    <th style="padding: 4px;">Qua</th>
                    <th style="padding: 4px;">Qui</th>
                    <th style="padding: 4px;">Sex</th>
                    <th style="padding: 4px;">Sáb</th>
                    <th style="padding: 4px;">Dom</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 12px; font-size: 12px; color: #94a3b8;">
            <span style="display: flex; align-items: center; gap: 5px;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background-color: #2563eb; display: inline-block;"></span> Hoje
            </span>
            <span style="display: flex; align-items: center; gap: 5px;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background-color: #ff0000; display: inline-block;"></span> Tarefas Pendentes
            </span>
        </div>
    </div>
    """
    st.markdown(calendar_html, unsafe_allow_html=True)
    
    # Lista em baixo de cada matéria que faz parte deste calendário
    st.markdown("#### Matérias com Entregas Agendadas")
    
    # Filtrar tarefas agendadas para o mês atual ou datas próximas
    scheduled_tasks = [t for t in tasks_with_dates if (t["parsed_due_date"].year == curr_year and t["parsed_due_date"].month == curr_month) or t["parsed_due_date"] >= today]
    scheduled_tasks.sort(key=lambda x: x["parsed_due_date"])
    
    if not scheduled_tasks:
        st.info("Nenhuma entrega agendada neste mês ou nas próximas datas.")
    else:
        # Agrupar por matéria
        tasks_by_subject = {}
        for st_item in scheduled_tasks:
            s_id = st_item.get("subject_id")
            s_name = subject_map.get(s_id, f"Disciplina {s_id}" if s_id else "Geral")
            if s_name not in tasks_by_subject:
                tasks_by_subject[s_name] = []
            tasks_by_subject[s_name].append(st_item)
            
        for s_name, t_list in tasks_by_subject.items():
            with st.expander(f"**{s_name}** ({len(t_list)} entrega{'s' if len(t_list) > 1 else ''})", expanded=True):
                for task in t_list:
                    d_formatted = task["parsed_due_date"].strftime("%d/%m/%Y")
                    t_status = task.get("status", "pending")
                    status_badge = "Concluída" if t_status == "completed" else ("Em Andamento" if t_status == "in_progress" else "Pendente")
                    
                    st.markdown(f"- **{task.get('title', 'Sem Título')}** — *{d_formatted}* ({status_badge})")
                    if task.get("description"):
                        st.caption(f"  {task['description']}")


