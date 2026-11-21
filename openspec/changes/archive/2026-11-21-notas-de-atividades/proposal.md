# Proposal: Notas de Atividades Concluídas

## Why

Atualmente no EduTrack AI, o estudante organiza suas tarefas acadêmicas e gerencia seus status (pendente, em andamento, concluída), mas não possui a possibilidade de registrar a avaliação ou nota obtida após a conclusão de cada atividade. Para proporcionar um acompanhamento acadêmico completo e permitir o controle de rendimento, é necessário disponibilizar a inserção de nota em cada atividade concluída, persistindo o dado no backend Xano e exibindo-o na interface do frontend mantendo o estilo visual escuro e limpo do sistema.

## What Changes

- **Schema e Endpoints no Xano**: Atualização da tabela `academic_tasks` (`table/academic_tasks.xs`) com o campo `grade` (numérico opcional de 0 a 10) e suporte ao campo nos endpoints de atualização e cadastro (`api/academic_tasks/academic_tasks_id_PATCH.xs`, `api/academic_tasks/academic_tasks_POST.xs`).
- **Interface de Tarefas no Frontend**: Atualização de `pages/2_📝_Tarefas.py` para permitir que o usuário informe a nota ao marcar como concluída ou ao editar uma tarefa concluída, além de exibir a nota de forma limpa no cabeçalho ou detalhes do card da tarefa, respeitando o tema escuro sem emojis.

## Capabilities

### New Capabilities
- `activity-grades`: Permite ao estudante registrar, atualizar e visualizar a nota de atividades acadêmicas concluídas no sistema, integrando backend Xano e frontend Streamlit.

### Modified Capabilities
<!-- None -->

## Impact

- **Backend / Xano**: Arquivo de schema `table/academic_tasks.xs` e endpoint `api/academic_tasks/academic_tasks_id_PATCH.xs`.
- **Frontend**: Arquivo `pages/2_📝_Tarefas.py` com inclusão de campo de nota e exibição nos cards de tarefas.
- **Dependências**: Nenhuma dependência externa adicional; uso de recursos nativos do Streamlit.
