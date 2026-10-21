# Tasks

## 1. Environment Configuration

- [x] 1.1 Configurar a variável `XANO_AUTH_BASE_URL` no arquivo `.env` na raiz do projeto e verificar seu carregamento

## 2. Frontend Authentication (Streamlit)

- [x] 2.1 Implementar formulário de cadastro (signup) em `pages/3_👤_Perfil.py` integrando com o endpoint `POST /auth/signup` e persistindo o usuário
- [x] 2.2 Implementar formulário de login em `pages/3_👤_Perfil.py` integrando com o endpoint `POST /auth/login` e gerenciando o token em `st.session_state`
- [x] 2.3 Implementar exibição do perfil do usuário em `pages/3_👤_Perfil.py` consumindo o endpoint `GET /auth/me` e ação de logout

## 3. Verification

- [x] 3.1 Executar e validar o fluxo de cadastro, login, consulta do perfil e logout no Streamlit

