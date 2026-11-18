# Proposal

## Why

A tela inicial (`app.py`) do EduTrack AI necessita de aprimoramentos estéticos e funcionais inspirados em dashboards modernos de aprendizagem. Para melhorar a experiência do usuário e a navegabilidade acadêmica, é necessário posicionar o atalho para o perfil no canto superior direito, exibir um calendário de próximas entregas com a lista de disciplinas vinculadas, e apresentar um quadro visual de progresso para matérias incompletas.

## What Changes

- **Redirecionamento para Perfil no Canto Superior Direito**:
  - Inclusão de botão/link de acesso rápido ao perfil do usuário no canto superior direito do cabeçalho da tela inicial (`pages/3_👤_Perfil.py`), exibindo identificação visual do usuário.
- **Calendário de Próximas Entregas de Atividades na Tela Inicial**:
  - Exibição de um componente visual de calendário marcando as próximas datas de entrega de tarefas acadêmicas cadastradas (`academic_tasks`).
  - Lista logo abaixo do calendário detalhando cada matéria/disciplina (`subjects`) que possui atividades no calendário com suas respectivas datas e títulos.
- **Quadro de Visão Geral de Progresso de Matérias Incompletas**:
  - Painel/quadro destacando o progresso percentual de cada matéria que ainda não atingiu 100% de conclusão.

## Capabilities

### New Capabilities
- `home-dashboard-ui`: Componentes visuais da tela inicial contendo navegação de perfil no topo direito, calendário de entregas com lista de disciplinas e quadro de progresso de matérias não concluídas.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend**: Modificações no arquivo principal `app.py`.
- **Backend / APIs**: Leitura das tarefas (`academic_tasks`) e disciplinas (`subjects`) já existentes no Xano via endpoints locais ou dados em sessão.
- **Dependências**: Componentes nativos do Streamlit.
