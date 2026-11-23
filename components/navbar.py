import base64
import sys
from pathlib import Path
import streamlit as st

# Garante que a raiz do projeto esteja no sys.path para importações consistentes
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def _get_logo_data_uri(filename: str) -> str:
    """Carrega a imagem de logo a partir de assets/logos/ e retorna como data URI base64."""
    path = ROOT_DIR / "assets" / "logos" / filename
    if path.exists():
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    return ""


def render_navbar():
    """Renderiza a barra superior de navegação (navbar/header) em todas as páginas

    e oculta a navegação nativa de páginas da barra lateral do Streamlit.
    """
    # Injeta CSS para ocultar a navegação padrão da barra lateral e estilizar a navbar superior
    st.markdown(
        """
        <style>
        /* Oculta navegação de páginas da barra lateral */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Fundo preto puro (#000000) para o modo escuro */
        .stApp {
            background-color: #000000;
        }

        /* Espaçamento e alinhamento do bloco da navbar superior */
        .edutrack-navbar-brand {
            font-size: 1.45rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
            line-height: 2.2rem;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .edutrack-navbar-brand img {
            height: 5.1rem;
            width: 5.1rem;
            object-fit: contain;
        }

        /* Ajuste dos ícones de imagem dentro de st.page_link */
        div[data-testid="stPageLink"] a img,
        div[data-testid="stPageLink"] img {
            height: 1.25rem !important;
            width: 1.25rem !important;
            max-height: 1.25rem !important;
            max-width: 1.25rem !important;
            object-fit: contain !important;
            vertical-align: middle !important;
            margin-right: 0.35rem !important;
            display: inline-block !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    logo_brand = _get_logo_data_uri("logo_00000.png")
    logo_home = _get_logo_data_uri("home_00000.png")
    logo_disci = _get_logo_data_uri("disci_00000.png")
    logo_tarefa = _get_logo_data_uri("tarefa_00000.png")
    logo_prog = _get_logo_data_uri("prog_00000.png")
    logo_linuq = _get_logo_data_uri("linuq_00000.png")
    logo_perf = _get_logo_data_uri("perfil_00000.png")

    is_logged_in = bool(st.session_state.get("auth_token"))

    # Grid de colunas para a barra superior: Marca + links de páginas
    if is_logged_in:
        col_brand, col_home, col_subj, col_tasks, col_prog, col_ai, col_perf = st.columns(
            [2.3, 1.0, 1.1, 1.0, 1.1, 1.1, 1.0],
            vertical_alignment="center",
        )
    else:
        # Quando deslogado, destaca Início e Entrar/Perfil
        col_brand, col_home, col_perf, col_empty = st.columns(
            [2.6, 1.2, 1.6, 3.6],
            vertical_alignment="center",
        )

    with col_brand:
        if logo_brand:
            st.markdown(
                f'<div class="edutrack-navbar-brand"><img src="{logo_brand}" alt="EduTrack AI" />EduTrack AI</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="edutrack-navbar-brand">EduTrack AI</div>',
                unsafe_allow_html=True,
            )

    with col_home:
        if logo_home:
            st.page_link(
                "Página Inicial.py",
                label=f"![Início]({logo_home}) Início",
                use_container_width=True,
            )
        else:
            st.page_link(
                "Página Inicial.py",
                label="Início",
                use_container_width=True,
            )

    if is_logged_in:
        with col_subj:
            if logo_disci:
                st.page_link(
                    "pages/1_📚_Disciplinas.py",
                    label=f"![Disciplinas]({logo_disci}) Disciplinas",
                    use_container_width=True,
                )
            else:
                st.page_link(
                    "pages/1_📚_Disciplinas.py",
                    label="Disciplinas",
                    use_container_width=True,
                )

        with col_tasks:
            if logo_tarefa:
                st.page_link(
                    "pages/2_📝_Tarefas.py",
                    label=f"![Tarefas]({logo_tarefa}) Tarefas",
                    use_container_width=True,
                )
            else:
                st.page_link(
                    "pages/2_📝_Tarefas.py",
                    label="Tarefas",
                    use_container_width=True,
                )

        with col_prog:
            if logo_prog:
                st.page_link(
                    "pages/3_📊_Progresso.py",
                    label=f"![Progresso]({logo_prog}) Progresso",
                    use_container_width=True,
                )
            else:
                st.page_link(
                    "pages/3_📊_Progresso.py",
                    label="Progresso",
                    use_container_width=True,
                )

        with col_ai:
            if logo_linuq:
                st.page_link(
                    "pages/4_💬_Tutor_IA.py",
                    label=f"![Tutor IA]({logo_linuq}) Tutor IA",
                    use_container_width=True,
                )
            elif logo_brand:
                st.page_link(
                    "pages/4_💬_Tutor_IA.py",
                    label=f"![Tutor IA]({logo_brand}) Tutor IA",
                    use_container_width=True,
                )
            else:
                st.page_link(
                    "pages/4_💬_Tutor_IA.py",
                    label="Tutor IA",
                    use_container_width=True,
                )

    with col_perf:
        perf_label = "Perfil" if is_logged_in else "Entrar / Cadastrar"
        if logo_perf:
            st.page_link(
                "pages/4_👤_Perfil.py",
                label=f"![{perf_label}]({logo_perf}) {perf_label}",
                use_container_width=True,
            )
        else:
            st.page_link(
                "pages/4_👤_Perfil.py",
                label=perf_label,
                use_container_width=True,
            )

    st.divider()


def render_page_header(title: str, logo_filename: str):
    """Renderiza a seção de título gigante da página exibindo a logo correspondente

    no lugar do emoji anterior.
    """
    logo_data_uri = _get_logo_data_uri(logo_filename)
    if logo_data_uri:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 14px; margin-top: 0.5rem; margin-bottom: 1.2rem;">
                <img src="{logo_data_uri}" alt="{title}" style="width: 46px; height: 46px; object-fit: contain;" />
                <h1 style="margin: 0; padding: 0; font-size: 2.25rem; font-weight: 700; line-height: 1.2;">
                    {title}
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.title(title)


def render_section_header(title: str, logo_filename: str):
    """Renderiza subtítulo de seção com a logo correspondente no lugar do emoji."""
    logo_data_uri = _get_logo_data_uri(logo_filename)
    if logo_data_uri:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
                <img src="{logo_data_uri}" alt="{title}" style="width: 26px; height: 26px; object-fit: contain;" />
                <h3 style="margin: 0; padding: 0; font-size: 1.35rem; font-weight: 600;">
                    {title}
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.subheader(title)


def require_auth() -> bool:
    """Verifica se o usuário está autenticado. Caso contrário, exibe mensagem

    de acesso restrito com botão de direcionamento para o login e interrompe
    a execução da página chamadora.
    """
    token = st.session_state.get("auth_token")
    if not token:
        st.warning("Acesso restrito. Esta página requer que você esteja conectado à sua conta do EduTrack AI.")
        col_btn, _ = st.columns([1.5, 3])
        with col_btn:
            st.page_link(
                "pages/4_👤_Perfil.py",
                label="Acessar Página de Perfil / Login",
                use_container_width=True,
            )
        st.stop()
        return False
    return True
