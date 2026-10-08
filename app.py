import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

# Título Principal
st.title("🎓 EduTrack AI")

# Inicialização de Estado Local (Mock / Cache para integração com Xano)
if "subjects" not in st.session_state:
    st.session_state["subjects"] = [
        {
            "id": 1,
            "user_id": 1,
            "name": "Innovation Lab",
            "teacher": "Prof. Orientador",
            "hours": 80,
            "status": "Ativa",
        }
    ]

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

# Funções Auxiliares de Gestão de Disciplinas
def get_subjects():
    return st.session_state["subjects"]

def add_subject(name, teacher, hours, status="Ativa", user_id=1):
    new_id = max([s["id"] for s in st.session_state["subjects"]], default=0) + 1
    st.session_state["subjects"].append({
        "id": new_id,
        "user_id": user_id,
        "name": name.strip(),
        "teacher": teacher.strip() if teacher else "",
        "hours": int(hours) if hours else 0,
        "status": status,
    })

def delete_subject(subject_id):
    st.session_state["subjects"] = [
        s for s in st.session_state["subjects"] if s["id"] != subject_id
    ]

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.subheader("Painel Geral")
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("💡 Conecte suas credenciais do Xano para sincronizar dados em tempo real.")

    # Cálculo dinâmico das métricas
    subjects = get_subjects()
    active_subjects = [s for s in subjects if s.get("status") == "Ativa"]
    total_hours = sum([s.get("hours", 0) for s in active_subjects])

    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas Ativas", str(len(active_subjects)))
    col2.metric("Horas em Curso", f"{total_hours}h")
    col3.metric("Tarefas Pendentes", "0")

    if active_subjects:
        st.write("---")
        st.markdown("### 📌 Disciplinas em Andamento")
        for subj in active_subjects:
            name_text = f"**{subj['name']}**"
            teacher_text = f" — Professor(a): {subj['teacher']}" if subj.get('teacher') else ""
            hours_text = f" ({subj.get('hours', 0)}h)" if subj.get('hours') else ""
            st.markdown(f"- {name_text}{hours_text}{teacher_text}")

elif menu_option == "Disciplinas":
    st.subheader("📚 Minhas Disciplinas")
    
    tab_list, tab_add = st.tabs(["📋 Disciplinas Cadastradas", "➕ Cadastrar Nova Disciplina"])

    with tab_list:
        subjects = get_subjects()
        if not subjects:
            st.warning("Nenhuma disciplina cadastrada ainda. Utilize a aba ao lado para cadastrar sua primeira matéria!")
        else:
            st.write(f"Total cadastrado: **{len(subjects)}** disciplina(s)")
            for subj in subjects:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([4, 2, 1])
                    with c1:
                        st.markdown(f"#### {subj['name']}")
                        details = []
                        if subj.get("teacher"):
                            details.append(f"👨‍🏫 **Docente:** {subj['teacher']}")
                        if subj.get("hours"):
                            details.append(f"⏱️ **Carga Horária:** {subj['hours']} horas")
                        if details:
                            st.caption(" | ".join(details))
                    
                    with c2:
                        status = subj.get("status", "Ativa")
                        if status == "Ativa":
                            st.success(f"Status: {status}")
                        elif status == "Concluída":
                            st.info(f"Status: {status}")
                        else:
                            st.warning(f"Status: {status}")
                    
                    with c3:
                        if st.button("🗑️ Excluir", key=f"del_{subj['id']}", use_container_width=True):
                            delete_subject(subj["id"])
                            st.success(f"Disciplina '{subj['name']}' removida com sucesso!")
                            st.rerun()

    with tab_add:
        st.markdown("Preencha os campos abaixo para cadastrar uma nova disciplina:")
        with st.form("form_nova_disciplina", clear_on_submit=True):
            nome = st.text_input("Nome da Disciplina * (name)", placeholder="Ex: Arquitetura de Software")
            col_a, col_b = st.columns(2)
            with col_a:
                docente = st.text_input("Professor(a) / Docente (teacher)", placeholder="Ex: Prof. Carlos Silva")
            with col_b:
                carga_horaria = st.number_input("Carga Horária (hours)", min_value=0, max_value=500, value=60, step=10)
            
            status = st.selectbox("Status", ["Ativa", "Concluída", "Trancada"])
            
            submitted = st.form_submit_button("Salvar Disciplina", use_container_width=True)
            if submitted:
                if not nome.strip():
                    st.error("O nome da disciplina é obrigatório.")
                else:
                    add_subject(nome, docente, carga_horaria, status)
                    st.success(f"Disciplina '{nome}' cadastrada com sucesso!")
                    st.rerun()

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Exemplo: Estudar Streamlit")