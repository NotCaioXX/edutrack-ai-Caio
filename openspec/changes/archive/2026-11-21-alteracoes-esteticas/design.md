# Design: Alterações Estéticas e Barra Superior de Navegação

## Context

A aplicação Streamlit do EduTrack AI utiliza o sistema de multipáginas nativo do Streamlit (`pages/`). Por padrão, o Streamlit gera uma lista de navegação na barra lateral esquerda (`[data-testid="stSidebarNav"]`). O usuário solicitou transferir essa navegação para uma barra superior ("navbar/header"), definir `Progresso` como página 3 e `Perfil` como página 4, remover o cabeçalho redundante, atalho de login e a seção "Acesso Rápido" na Página Inicial, traduzir todos os menus dropdown de status para português ("Pendente", "Em progresso", "Concluído"), retirar referências textuais a tabelas técnicas do Xano, substituir os emojis de Disciplinas, Tarefas, Progresso, Home e da marca EduTrack AI pelos logos personalizados em `assets/logos/`, ampliar a logo do projeto em 3x e configurar o fundo escuro para preto puro `#000000`.

## Goals / Non-Goals

**Goals:**
- Ocultar a navegação padrão de páginas da barra lateral do Streamlit via configuração e CSS.
- Criar um componente/função reutilizável de barra superior (`render_navbar`) com links diretos usando `st.page_link` para todas as páginas da aplicação.
- Garantir a ordem correta das páginas: `3_📊_Progresso.py` (página 3) e `4_👤_Perfil.py` (página 4), atualizando quaisquer referências no código.
- Limpar a `Página Inicial.py`, retirando o título redundante, legenda de login e a seção de "Acesso Rápido".
- Traduzir os campos de status nos menus dropdown para "Pendente", "Em progresso" e "Concluído".
- Remover menções a tabelas técnicas (`(Tabela subjects)`, `(Tabela academic_tasks)`) nos textos de interface.
- Substituir os emojis ao lado dos títulos e na navbar pelas logos personalizadas (`disci_00000.png`, `tarefa_00000.png`, `prog_00000.png`, `home_00000.png`).
- Aumentar a logo do projeto em 3x na barra de navegação com alinhamento vertical centralizado.
- Configurar o modo escuro do Streamlit para ter a cor de fundo preta pura `#000000`.
- Estilizar o calendário da Página Inicial em tom cinza com marcadores circulares preenchidos para o dia de hoje (azul) e tarefas pendentes (vermelho `#ff0000`).
- Substituir o emoji de Perfil na barra superior de navegação pela logo `perfil_00000.png`.
- Remover todos os emojis de interface em todas as páginas da aplicação, mantendo apenas as logos gráficas existentes.

**Non-Goals:**
- Não alterar a lógica de autenticação com o Xano nem os valores salvos no backend (`pending`, `in_progress`, `completed`).
- Não modificar os schemas ou endpoints no backend Xano.
- Não remover conteúdos funcionais das páginas além dos explicitamente solicitados.

## Decisions

1. **Ocultação da Navegação da Barra Lateral**:
   - *Decisão*: Combinar `showSidebarNavigation = false` no `.streamlit/config.toml` e regra CSS `[data-testid="stSidebarNav"] { display: none !important; }` através de `st.markdown(..., unsafe_allow_html=True)`.
   - *Alternativa considerada*: Utilizar apenas CSS. A combinação com `.streamlit/config.toml` fornece suporte nativo estável do Streamlit.

2. **Componente Reutilizável de Navbar Superior (`components/navbar.py`)**:
   - *Decisão*: Centralizar o cabeçalho superior em `render_navbar()` que monta colunas horizontais com `st.page_link` para `Página Inicial.py`, `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_📊_Progresso.py` e `pages/4_👤_Perfil.py`.
   - *Alternativa considerada*: Duplicar o código da navbar em cada página. O componente centralizado evita divergências e facilita manutenção.

3. **Limpeza da Página Inicial**:
   - *Decisão*: Remover o título redundante `st.title("🎓 EduTrack AI")` e mensagem de login/boas-vindas do corpo da página (uma vez que a navbar superior já exibe a marca e links), além de excluir a seção de texto "Acesso Rápido" no rodapé de `Página Inicial.py`.
   - *Alternativa considerada*: Manter um título menor. Descartado para dar destaque imediato às métricas e ao calendário acadêmico.

4. **Tradução de Status com `format_func`**:
   - *Decisão*: Mapear os status técnicos via dicionário `STATUS_LABELS = {"pending": "Pendente", "in_progress": "Em progresso", "completed": "Concluído"}` e utilizar o parâmetro `format_func` no `st.selectbox`.
   - *Alternativa considerada*: Alterar os valores internos para strings em português. Descartado para não quebrar a persistência e validação no schema da tabela `academic_tasks` do Xano.

5. **Remoção de Rótulos de Tabelas do Xano**:
   - *Decisão*: Remover as anotações `(Tabela subjects)` e `(Tabela academic_tasks)` das métricas e títulos de formulário, mantendo apenas os títulos humanizados.
   - *Alternativa considerada*: Ocultar via CSS. A remoção direta do texto garante interface limpa e acessível.

6. **Substituição de Emojis por Logos Customizados**:
   - *Decisão*: Carregar imagens `disci_00000.png`, `tarefa_00000.png`, `prog_00000.png` e `home_00000.png` de `assets/logos/` em formato base64 data URI. Na navbar, os links usam markdown `![alt](url)` com estilização CSS para atuarem como ícones. Nos títulos gigantes, a função `render_page_header` alinha a logo com a tag `<h1>`.
   - *Alternativa considerada*: Usar colunas com `st.image`. Descartado para o título pois o flex container HTML provê alinhamento vertical exato e responsividade sem quebras indesejadas de linha.

7. **Logo do Projeto e Seção de Progresso na Página Inicial**:
   - *Decisão*: Empregar `logo_00000.png` como imagem do projeto na navbar superior (`col_brand`) e como `page_icon` no `st.set_page_config`, substituindo o emoji de capelo (`🎓`). Para a seção de progresso da Página Inicial, utilizar a função `render_section_header` integrando `prog_00000.png` ao subtítulo.
   - *Alternativa considerada*: Manter os emojis legados. Descartado para unificar a identidade visual gráfica do EduTrack AI.

8. **Aumento da Logo em 3x e Logo Home**:
   - *Decisão*: A logo da marca (`logo_00000.png`) foi ampliada para `5.1rem` (3x a dimensão anterior de 1.7rem) com `vertical_alignment="center"` nas colunas da navbar. O link "Início" na navbar passou a utilizar a logo `home_00000.png` (`home`) substituindo o emoji de casa (`🏠`).
   - *Alternativa considerada*: Manter a logo em tamanho padrão. O aumento de 3x atende à solicitação expressa do usuário de dar maior destaque à identidade da marca.

9. **Tema Escuro com Fundo Preto Puro (#000000)**:
   - *Decisão*: Configurar `[theme]` em `.streamlit/config.toml` com `base = "dark"`, `backgroundColor = "#000000"`, `secondaryBackgroundColor = "#111111"` e `textColor = "#FFFFFF"`, e reforçar via CSS `.stApp { background-color: #000000; }`.
   - *Alternativa considerada*: Apenas CSS. A configuração declarativa em `.streamlit/config.toml` garante compatibilidade nativa com o sistema de temas do Streamlit.

10. **Estilização e Marcadores do Calendário da Página Inicial**:
    - *Decisão*: Renderizar a tabela do calendário em um card container com cor de fundo cinza (`#1e1e1e`) e bordas `#333333`. Configurar o dia atual com círculo preenchido em azul (`#2563eb`) e os dias com tarefas pendentes com círculo preenchido em vermelho (`#ff0000`). Para dias atuais com tarefas pendentes, combinar fundo vermelho e borda azul para refletir ambas as condições. Incluir legenda explicativa.
    - *Alternativa considerada*: Manter o card branco padrão ou apenas texto colorido nos dias. A abordagem com círculos preenchidos e container cinza garante contraste e leitura clara no fundo escuro.

11. **Substituição da Logo de Perfil na Navbar e Remoção Global de Emojis**:
    - *Decisão*: Carregar `perfil_00000.png` como data URI em `components/navbar.py` e renderizar o link de Perfil com a logo no mesmo padrão das demais páginas. Remover todos os emojis de textos, abas, botões, métricas e alertas em todas as páginas (`Página Inicial.py`, `Disciplinas`, `Tarefas`, `Progresso`, `Perfil`), preservando as logos gráficas onde já existentes.
    - *Alternativa considerada*: Manter ícones unicode padrão. A remoção total confere um visual limpo, profissional e consistente com a identidade visual baseada nas logos customizadas.

## Risks / Trade-offs

- **[Risco]** Divergência entre rótulo exibido e código persistido no banco de dados.
  - *Mitigação*: Uso de `format_func` mantém o retorno exato do `st.selectbox` como o código original esperado pela API do Xano (`pending`, `in_progress`, `completed`).
- **[Risco]** Quebra de links de navegação caso o caminho do arquivo mude.
  - *Mitigação*: `st.page_link` valida os caminhos exatos dos arquivos locais (`pages/3_📊_Progresso.py`, `pages/4_👤_Perfil.py`, etc.).
