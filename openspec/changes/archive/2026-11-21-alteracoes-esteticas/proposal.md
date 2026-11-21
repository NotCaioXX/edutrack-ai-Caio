# Proposal

## Why

A navegação padrão do Streamlit na barra lateral ocupa espaço lateral contínuo e dispersa a atenção visual do usuário entre abas e páginas. Para modernizar a experiência de uso do EduTrack AI, a navegação de páginas deve ser transferida para uma barra superior centralizada ("navbar/header"). Além disso, com a reestruturação da ordem das páginas (Progresso como página 3 e Perfil como página 4), é necessário atualizar todos os links do sistema, remover o cabeçalho/título redundante, botão de atalho de login e seção "Acesso Rápido" na Página Inicial, traduzir os campos de status dos menus dropdown para português ("Pendente", "Em progresso", "Concluído"), remover termos técnicos que expõem nomes de tabelas do banco Xano, substituir os emojis de Disciplinas, Tarefas e Progresso pelos seus logos correspondentes, substituir o emoji ao lado do nome do projeto ("EduTrack AI") pela logo oficial aumentada em 3x, substituir o emoji de "Início" na navbar pelo logo `home_00000.png`, substituir o emoji da seção de progresso na Página Inicial, configurar o tema escuro com fundo preto puro `#000000`, estilizar o calendário da Página Inicial em cinza com marcadores circulares preenchidos para hoje (azul) e pendências (vermelho `#ff0000`), substituir o emoji de Perfil na barra superior pela logo oficial `perfil_00000.png` e remover todos os emojis remanescentes de todas as páginas da aplicação, mantendo somente as logos gráficas onde já existem.

## What Changes

- **Barra Superior de Navegação (Navbar/Header)**:
  - Ocultação da navegação padrão de páginas da barra lateral do Streamlit via configuração e CSS.
  - Disponibilização de barra superior (navbar/header) em linha com links de navegação para todas as páginas da aplicação (`Página Inicial`, `Disciplinas`, `Tarefas`, `Progresso`, `Perfil`).
  - Aumento da logo do projeto na navbar em 3x (para escala de destaque visual).
  - Substituição do emoji de "Início" na navbar pela logo `home_00000.png`.
- **Ajuste de Numeração e Links das Páginas 3 e 4**:
  - Garantia de que a página 3 corresponda a Progresso (`pages/3_📊_Progresso.py`) e a página 4 corresponda a Perfil (`pages/4_👤_Perfil.py`).
  - Atualização de quaisquer links existentes no código que referenciem as páginas 3 e 4.
- **Limpeza da Página Inicial**:
  - Remoção do botão de atalho / redirecionamento para a página de login / perfil que estava presente no cabeçalho de `Página Inicial.py`.
  - Remoção do cabeçalho/título redundante e legenda de autenticação no corpo da `Página Inicial.py`, preservando a identidade visual na navbar superior.
  - Remoção da seção final "Acesso Rápido" de `Página Inicial.py`.
- **Tradução dos Menus Dropdown de Status**:
  - Tradução de todos os menus dropdown de status em todas as páginas para os valores legíveis em português: "Pendente", "Em progresso" e "Concluído" (mantendo a compatibilidade dos códigos internos no backend).
- **Remoção de Referências a Tabelas no Xano**:
  - Remoção de textos de interface que citam explicitamente nomes de tabelas técnicas (ex.: `(Tabela subjects)`, `(Tabela academic_tasks)`) na Página Inicial, Disciplinas e Tarefas.
- **Substituição de Emojis por Logos Customizados**:
  - Substituição dos emojis pelos arquivos de imagem em `assets/logos/` (`disci_00000.png`, `tarefa_00000.png`, `prog_00000.png`, `home_00000.png`) nos links da barra de navegação e na seção de título gigante das páginas.
  - Substituição do emoji ao lado do nome do projeto ("EduTrack AI") pela logo `logo_00000.png` em todo o site (na barra superior e no favicon da Página Inicial).
  - Substituição do emoji da seção "Visão Geral de Progresso (Matérias Incompletas)" na Página Inicial pela logo de progresso `prog_00000.png`.
- **Tema Escuro com Fundo Preto Puro**:
  - Configuração do tema dark do Streamlit com fundo `#000000` via `.streamlit/config.toml` e estilização CSS na classe `.stApp`.
- **Estilização do Calendário da Página Inicial**:
  - Estilização do card/container e da tabela do calendário acadêmico na cor cinza (`#1e1e1e` com bordas `#333333`) para integração visual ao tema escuro.
  - Marcador do dia de hoje configurado com círculo totalmente preenchido em azul (`#2563eb`) e texto em branco.
  - Marcador de tarefas pendentes configurado com círculo totalmente preenchido em vermelho (`#ff0000`) e texto em branco.
  - Inclusão de legenda indicativa na base do calendário.
- **Logo de Perfil na Navbar Superior**:
  - Substituição do ícone emoji do link "Perfil" na barra de navegação superior pela logo gráfica `assets/logos/perfil_00000.png`.
- **Remoção Global de Emojis em Todas as Páginas**:
  - Remoção completa de emojis nos textos de interface de todas as páginas (títulos, subtítulos, abas, botões de ação, métricas, alertas e fallbacks), mantendo exclusivamente as logos gráficas onde já existem.

## Capabilities

### New Capabilities
- `top-navbar-navigation`: Barra superior de navegação (navbar/header) em substituição à barra lateral, ajuste de links e ordem das páginas 3 (Progresso) e 4 (Perfil), limpeza da Página Inicial, tradução dos menus dropdown de status, remoção de referências a tabelas do Xano, ampliação e integração dos logos personalizados de Disciplinas, Tarefas, Progresso, Home, Perfil e da marca EduTrack AI, tema escuro com fundo preto `#000000`, estilização do calendário e remoção total de emojis de todas as páginas mantendo apenas as logos existentes.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend**:
  - Componente reutilizável `components/navbar.py` com suporte a logos na navbar, `render_page_header` e `render_section_header`.
  - Configuração em `.streamlit/config.toml` para tema escuro e fundo preto `#000000`.
  - Atualização dos arquivos: `Página Inicial.py`, `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_📊_Progresso.py` e `pages/4_👤_Perfil.py`.
- **Backend / APIs**: Nenhuma alteração de schema ou API Xano.
- **Dependências**: Componentes nativos do Streamlit (`st.page_link`, `st.columns`, CSS customizado via `st.markdown`) e leitura dos assets de imagem.
