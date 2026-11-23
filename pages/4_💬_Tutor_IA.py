import sys
from pathlib import Path
import streamlit as st

# Setup project path for scripts import
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.navbar import render_navbar, render_page_header, require_auth
from scripts.ai_tutor_service import (
    call_ai_tutor,
    get_gemini_api_key,
    is_query_about_grades_or_academic_data,
    format_academic_context
)
from scripts.calculate_progress import calculate_all_progress, load_env

page_icon_path = PROJECT_ROOT / "assets" / "logos" / "linuq_00000.png"
if not page_icon_path.exists():
    page_icon_path = PROJECT_ROOT / "assets" / "logos" / "logo_00000.png"

st.set_page_config(
    page_title="Tutor IA - EduTrack AI",
    page_icon=str(page_icon_path) if page_icon_path.exists() else None,
    layout="wide"
)

render_navbar()
require_auth()
load_env()

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

render_page_header("Tutor IA de Estudos", "linuq_00000.png")

st.markdown(
    """
    <p style="color: #94a3b8; font-size: 1.05rem; margin-top: -10px; margin-bottom: 20px;">
        Converse com seu assistente inteligente sobre métodos de estudo, técnicas de memorização,
        rotinas de revisão e tire dúvidas sobre suas notas e progresso acadêmico.
    </p>
    """,
    unsafe_allow_html=True
)

# Inicializa o histórico de mensagens na sessão se ainda não existir
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = [
        {
            "role": "assistant",
            "content": (
                "Olá! Sou seu Mentor de Estudos do EduTrack AI.\n\n"
                "Posso te ajudar com:\n"
                "- Análise e orientação sobre suas notas e progresso no curso\n"
                "- Técnicas de memorização (Feynman, Active Recall, Flashcards)\n"
                "- Organização de tempo (Pomodoro, blocos de foco)\n"
                "- Planejamento de estudos e cronograma de provas\n\n"
                "Como posso te ajudar hoje?"
            )
        }
    ]

# Sugestões rápidas de temas
col_sug1, col_sug2, col_sug3, col_sug4 = st.columns(4)
quick_prompt = None

with col_sug1:
    if st.button("Como estão minhas notas?", use_container_width=True):
        quick_prompt = "Como estão minhas notas e meu rendimento geral nas disciplinas?"

with col_sug2:
    if st.button("Como usar Técnica Feynman?", use_container_width=True):
        quick_prompt = "Como funciona e como posso aplicar a Técnica de Feynman nos meus estudos?"

with col_sug3:
    if st.button("Como organizar Pomodoro?", use_container_width=True):
        quick_prompt = "Como organizar ciclos de foco com a Técnica Pomodoro para evitar cansaço mental?"

with col_sug4:
    if st.button("O que é Active Recall?", use_container_width=True):
        quick_prompt = "O que é Active Recall e como combinar com repetição espaçada?"

st.write("")

# Container com altura fixa e rolagem interna para a conversa
chat_container = st.container(height=480)

with chat_container:
    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Captura de input do usuário (seja via botão rápido ou caixa de texto)
user_input = st.chat_input("Digite sua dúvida sobre estudos, técnicas ou suas notas...")

prompt_to_send = quick_prompt or user_input

if prompt_to_send:
    # Registra a mensagem do usuário
    st.session_state.ai_messages.append({"role": "user", "content": prompt_to_send})

    # Verifica se a pergunta é sobre notas/desempenho
    is_grades_query = is_query_about_grades_or_academic_data(prompt_to_send)
    academic_context = None

    if is_grades_query:
        if not token:
            ai_response = (
                "Para que eu possa consultar suas notas, médias e tarefas cadastradas, "
                "é necessário estar autenticado no sistema.\n\n"
                "Por favor, acesse a página **Perfil** na barra de navegação superior, "
                "faça login com sua conta do EduTrack AI e depois volte aqui para conversarmos sobre seu desempenho!"
            )
            st.session_state.ai_messages.append({"role": "assistant", "content": ai_response})
            st.rerun()
        else:
            # Usuário autenticado: busca o progresso e notas atualizadas
            try:
                progress_data = calculate_all_progress(token=token)
                if not progress_data and st.session_state.get("cached_subjects"):
                    progress_data = calculate_all_progress(
                        token=token,
                        cached_subjects=st.session_state.get("cached_subjects"),
                        cached_tasks=st.session_state.get("cached_tasks")
                    )
                academic_context = format_academic_context(user, progress_data)
            except Exception as e:
                academic_context = f"Erro ao consultar dados no Xano: {str(e)}"

    # Gera resposta chamando a IA
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt_to_send)
        with st.chat_message("assistant"):
            with st.spinner("Analisando e preparando sua orientação..."):
                ai_response = call_ai_tutor(
                    st.session_state.ai_messages,
                    academic_context=academic_context
                )
                st.markdown(ai_response)
                st.session_state.ai_messages.append({"role": "assistant", "content": ai_response})

    st.rerun()
