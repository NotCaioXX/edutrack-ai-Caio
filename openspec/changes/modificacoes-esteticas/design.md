# Design

## Context

A tela inicial atual (`app.py`) exibe apenas métricas numéricas simples e atalhos em texto na barra lateral. O usuário solicitou três melhorias estéticas e funcionais específicas para alinhar a página inicial ao modelo visual fornecido:
1. Mover/posicionar no canto superior direito o redirecionamento para a tela de Perfil (`pages/3_👤_Perfil.py`).
2. Adicionar um calendário destacando as próximas datas de entrega de atividades, com a lista das matérias vinculadas a essas datas logo abaixo.
3. Exibir um quadro de visão geral de progresso dedicado às matérias que ainda não estão completas (< 100%).

## Goals / Non-Goals

**Goals:**
- Implementar cabeçalho com alinhamento à direita para navegação rápida ao Perfil via `st.page_link`.
- Implementar componente de calendário do mês atual destacando dias com entregas de tarefas (`academic_tasks`), acompanhado por lista de matérias e atividades agendadas logo abaixo.
- Implementar quadro de visão geral de progresso calculando e exibindo barras de progresso para cada matéria incompleta.
- Manter estrita aderência ao pedido do usuário sem alterar endpoints ou arquivos fora do escopo.

**Non-Goals:**
- Não criar nem modificar endpoints de backend ou tabelas XanoScript.
- Não alterar páginas secundárias (`pages/1_...`, `pages/2_...`, etc.).
- Não adicionar bibliotecas pesadas de terceiros (usar módulos nativos `calendar`, `datetime` e recursos visuais do Streamlit).

## Decisions

### 1. Posicionamento do Perfil no Canto Superior Direito
- **Decisão**: Utilizar `st.columns([3, 1])` no topo de `app.py`. A coluna esquerda conterá o título e saudação, e a coluna direita exibirá o componente de acesso rápido ao perfil utilizando `st.page_link("pages/3_👤_Perfil.py", label=..., icon="👤")`.
- **Alternativas consideradas**: Botão padrão com `st.switch_page`. O `st.page_link` é mais fluido e compatível com a navegação multipage nativa do Streamlit.

### 2. Renderização do Calendário de Entregas e Lista de Matérias
- **Decisão**: Utilizar `calendar.monthcalendar` da biblioteca padrão do Python para gerar a matriz do mês atual. As datas com prazos de `academic_tasks` serão destacadas visualmente. Logo abaixo do calendário, listar as matérias participantes com nome da tarefa, matéria e data formatada.
- **Alternativas consideradas**: Biblioteca externa `streamlit-calendar`. Rejeitada para evitar dependências adicionais e possíveis incompatibilidades de ambiente.

### 3. Quadro de Progresso de Matérias Incompletas
- **Decisão**: Cruzar `cached_subjects` e `cached_tasks`. Para cada disciplina, calcular a proporção de tarefas concluídas (`status == 'completed'`). Exibir apenas matérias cujo progresso for inferior a 100%, renderizando cada uma com título e `st.progress(pct)`.
- **Alternativas consideradas**: Exibir todas as matérias. Rejeitada porque o usuário pediu explicitamente "em cada matéria que não está completa".

## Risks / Trade-offs

- **[Risk] Ausência de tarefas com data configurada**: O calendário não teria dias destacados.
  - **Mitigação**: Exibir o calendário com os dias do mês normalmente e uma mensagem informativa clara caso nenhuma tarefa possua prazo definido.
- **[Risk] Matérias sem tarefas cadastradas**: Progresso indefinido (0/0).
  - **Mitigação**: Tratar divisão por zero considerando progresso 0% para matérias recém-criadas sem tarefas, mantendo-as na lista de matérias a iniciar/incompletas.
