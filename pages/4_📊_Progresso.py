import os
import sys
from pathlib import Path
import streamlit as st

# Setup project path for scripts import
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.calculate_progress import (
    load_env,
    calculate_all_progress
)
from scripts.generate_pdf_report import generate_performance_pdf

st.set_page_config(page_title="Progresso & Desempenho", page_icon="📊", layout="wide")

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

st.title("📊 Progresso Acadêmico & Relatório")

# Barra de status do usuário
if user and token:
    st.caption(f"👤 Estudante: **{user.get('name', 'Estudante')}** ({user.get('email', '')}) — Dados sincronizados com Xano")
elif token:
    st.caption("🔑 Sessão ativa com Xano.")
else:
    st.info("💡 **Dica:** Acesse a página **👤 Perfil** para fazer login e calcular o progresso das disciplinas salvas na sua conta do Xano.")

st.markdown("---")

# Obtenção dos dados de progresso através de scripts/calculate_progress.py
with st.spinner("Calculando progresso acadêmico..."):
    if token:
        progress_data = calculate_all_progress(token=token)
        # Se os endpoints retornarem vazio mas houver dados em cache local, usa cache
        if not progress_data and st.session_state.get("cached_subjects"):
            progress_data = calculate_all_progress(
                token=token,
                tasks_data=st.session_state.get("cached_tasks", []),
                subjects_data=st.session_state.get("cached_subjects", [])
            )
    else:
        # Fallback para dados em cache local se o usuário navegar como visitante
        progress_data = calculate_all_progress(
            token=None,
            tasks_data=st.session_state.get("cached_tasks", []),
            subjects_data=st.session_state.get("cached_subjects", [])
        )

# Cálculos Consolidados Gerais
total_disciplinas = len(progress_data)
total_tarefas = sum(item.get("total_tasks", 0) for item in progress_data)
total_concluidas = sum(item.get("completed_tasks", 0) for item in progress_data)
total_pendentes = sum(item.get("pending_tasks", 0) for item in progress_data)
progresso_geral = round((total_concluidas / total_tarefas * 100), 2) if total_tarefas > 0 else 0.0

# 1. Resumo Executivo (Cards de Métricas)
st.subheader("📈 Resumo de Desempenho")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Disciplinas Ativas", total_disciplinas)
c2.metric("Total de Tarefas", total_tarefas)
c3.metric("Tarefas Concluídas", total_concluidas)
c4.metric("Progresso Geral", f"{progresso_geral}%")

# Barra visual de progresso geral
progresso_frac = min(max(progresso_geral / 100.0, 0.0), 1.0)
st.progress(progresso_frac, text=f"Taxa de Conclusão Global: {progresso_geral}%")

st.markdown("---")

# 2. Seção de Download do Relatório em PDF (usando scripts/generate_pdf_report.py)
st.subheader("📑 Relatório Oficial em PDF")
col_pdf_info, col_pdf_btn = st.columns([3, 1])

with col_pdf_info:
    st.write("Gere um documento em PDF com o sumário completo das disciplinas, contadores de tarefas e taxa de conclusão.")

with col_pdf_btn:
    try:
        nome_aluno = user.get("name", "Estudante") if user else "Estudante"
        email_aluno = user.get("email", "estudante@edutrack.ai") if user else "estudante@edutrack.ai"
        user_suffix = user.get("id", "local") if user else "visitante"
        
        pdf_rel_path = f"reports/relatorio_desempenho_{user_suffix}.pdf"
        
        # Gera o PDF utilizando scripts/generate_pdf_report.py
        pdf_abs_path = generate_performance_pdf(
            student_name=nome_aluno,
            student_email=email_aluno,
            token=token,
            output_path=pdf_rel_path,
            progress_data=progress_data
        )

        with open(pdf_abs_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        st.download_button(
            label="📥 Baixar Relatório (PDF)",
            data=pdf_bytes,
            file_name=f"relatorio_desempenho_{nome_aluno.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Erro ao preparar arquivo PDF: {e}")

st.markdown("---")

# 3. Detalhamento por Disciplina
st.subheader("📚 Progresso Detalhado por Disciplina")

if not progress_data:
    st.info("Nenhuma disciplina encontrada. Acesse a aba **📚 Disciplinas** para cadastrar matérias e **📝 Tarefas** para cadastrar obrigações.")
else:
    for item in progress_data:
        s_id = item.get("subject_id")
        s_name = item.get("subject_name") or f"Disciplina #{s_id}"
        s_total = item.get("total_tasks", 0)
        s_comp = item.get("completed_tasks", 0)
        s_pend = item.get("pending_tasks", 0)
        s_pct = item.get("progress_percentage", 0.0)

        with st.container():
            c_header1, c_header2 = st.columns([3, 1])
            with c_header1:
                st.markdown(f"#### 📖 {s_name}")
            with c_header2:
                if s_total == 0:
                    st.caption("ℹ️ Nenhuma tarefa associada")
                elif s_pct == 100.0:
                    st.success(f"✅ {s_pct}% Concluída")
                elif s_pct > 0.0:
                    st.info(f"⏳ {s_pct}% Concluída")
                else:
                    st.warning(f"📌 {s_pct}% Concluída")

            # Barra de progresso da disciplina
            pct_frac = min(max(s_pct / 100.0, 0.0), 1.0)
            st.progress(pct_frac)

            # Métricas em colunas
            m1, m2, m3 = st.columns(3)
            m1.write(f"📝 **Total de Tarefas:** {s_total}")
            m2.write(f"✅ **Concluídas:** {s_comp}")
            m3.write(f"⏳ **Pendentes:** {s_pend}")

            st.divider()

