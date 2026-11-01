import os
from pathlib import Path
import streamlit as st
import requests

st.set_page_config(page_title="Perfil & Autenticação", page_icon="👤")

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
                    if key:
                        os.environ[key] = val

load_env()
BASE_URL = os.environ.get("XANO_AUTH_BASE_URL", "").rstrip("/")

# Inicialização do estado da sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

def get_auth_headers():
    token = st.session_state.get("auth_token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def fetch_user_profile():
    if not BASE_URL:
        return None
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            st.session_state["user_info"] = user_data
            return user_data
        elif response.status_code in [401, 403]:
            # Token expirado ou inválido
            st.session_state["auth_token"] = None
            st.session_state["user_info"] = None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
    return None

st.title("👤 Perfil do Usuário")

if not BASE_URL:
    st.warning("⚠️ A variável `XANO_AUTH_BASE_URL` não foi configurada no arquivo `.env`.")
    st.info("Adicione a URL base dos endpoints no formato: `XANO_AUTH_BASE_URL=https://<instancia>.xano.io/api:6cQL_hM3` no arquivo `.env`.")

# Exibição quando usuário já está autenticado
if st.session_state.get("auth_token"):
    user = st.session_state.get("user_info")
    if not user:
        user = fetch_user_profile()

    if user:
        st.success(f"Olá, **{user.get('name', 'Estudante')}**! Você está conectado.")
        
        st.markdown("---")
        st.subheader("📋 Dados da Conta")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Nome:** {user.get('name', '-')}")
            st.write(f"**E-mail:** {user.get('email', '-')}")
        with col2:
            st.write(f"**Função (Role):** {user.get('role', 'member')}")
            st.write(f"**ID do Usuário:** {user.get('id', '-')}")

        st.markdown("---")
        if st.button("🚪 Sair (Logout)", type="secondary"):
            st.session_state["auth_token"] = None
            st.session_state["user_info"] = None
            st.success("Você saiu da sua conta.")
            st.rerun()
    else:
        st.info("Carregando informações do usuário...")
        if st.button("Tentar novamente"):
            fetch_user_profile()
            st.rerun()

else:
    # Abas para alternar entre Login e Cadastro
    tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Cadastrar-se (Cadastro)"])

    with tab_login:
        st.subheader("Acesse sua Conta")
        with st.form("form_login"):
            login_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com").strip().lower()
            login_password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit_login = st.form_submit_button("Entrar", use_container_width=True)

            if submit_login:
                if not login_email or not login_password:
                    st.error("Por favor, preencha todos os campos.")
                elif not BASE_URL:
                    st.error("URL da API não configurada.")
                else:
                    with st.spinner("Autenticando..."):
                        try:
                            payload = {"email": login_email, "password": login_password}
                            response = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=10)
                            if response.status_code == 200:
                                data = response.json()
                                token = data.get("authToken")
                                if token:
                                    st.session_state["auth_token"] = token
                                    fetch_user_profile()
                                    st.success("Login realizado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Resposta inesperada do servidor: token não encontrado.")
                            elif response.status_code in [400, 401, 403]:
                                error_msg = response.json().get("message", "Credenciais inválidas. Verifique seu e-mail e senha.")
                                st.error(error_msg)
                            else:
                                st.error(f"Erro {response.status_code}: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Falha de conexão com a API: {e}")

    with tab_signup:
        st.subheader("Crie sua Conta no EduTrack AI")
        with st.form("form_signup"):
            signup_name = st.text_input("Nome Completo", placeholder="Seu nome").strip()
            signup_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com").strip().lower()
            signup_password = st.text_input("Senha", type="password", placeholder="Mínimo de 8 caracteres").strip()
            submit_signup = st.form_submit_button("Cadastrar", use_container_width=True)

            if submit_signup:
                if not signup_name or not signup_email or not signup_password:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
                elif len(signup_password) < 8:
                    st.warning("A senha deve ter pelo menos 8 caracteres.")
                elif not BASE_URL:
                    st.error("URL da API não configurada.")
                else:
                    with st.spinner("Criando conta..."):
                        try:
                            payload = {
                                "name": signup_name,
                                "email": signup_email,
                                "password": signup_password
                            }
                            response = requests.post(f"{BASE_URL}/auth/signup", json=payload, timeout=10)
                            if response.status_code == 200:
                                data = response.json()
                                token = data.get("authToken")
                                if token:
                                    st.session_state["auth_token"] = token
                                    fetch_user_profile()
                                    st.success("Conta criada com sucesso! Você já está conectado.")
                                    st.rerun()
                                else:
                                    st.success("Conta criada com sucesso! Faça login na aba ao lado.")
                            elif response.status_code in [400, 401, 403]:
                                error_msg = response.json().get("message", "Esta conta ou e-mail já está em uso.")
                                st.error(error_msg)
                            else:
                                st.error(f"Erro {response.status_code}: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Falha de conexão com a API: {e}")

