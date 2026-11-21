# Design: Notas de Atividades Concluídas

## Context

No EduTrack AI, as tarefas acadêmicas dos alunos são modeladas no backend Xano pelo arquivo `table/academic_tasks.xs` e gerenciadas através de endpoints REST em `api/academic_tasks/`. A interface visual do estudante em Streamlit (`pages/2_📝_Tarefas.py`) permite criar, listar, filtrar e atualizar o status das atividades. Atualmente não existe campo de nota vinculado à tarefa, impedindo que o aluno anote o seu rendimento após concluir uma entrega.

## Goals / Non-Goals

**Goals:**
- Estender a tabela `academic_tasks` (`table/academic_tasks.xs`) com o campo opcional de nota `decimal grade?`.
- Atualizar o endpoint `PATCH /academic_tasks/{academic_tasks_id}` (`api/academic_tasks/academic_tasks_id_PATCH.xs`) para aceitar o campo `grade` no payload de atualização.
- Integrar no frontend (`pages/2_📝_Tarefas.py`) a possibilidade de inserir e editar a nota para tarefas concluídas.
- Exibir a nota das atividades concluídas no card da tarefa de forma harmônica com o tema escuro e a ausência de emojis.

**Non-Goals:**
- Não criar regras complexas de cálculo de média ponderada ou curvas de notas não solicitadas.
- Não criar endpoints de consulta adicionais não requisitados (conforme Regra nº 1 de escopo).
- Não executar comandos de push/sync para o Xano (conforme Regra nº 2).

## Decisions

1. **Adição do campo de nota diretamente na tabela `academic_tasks`**:
   - *Decisão*: Adicionar `decimal grade?` à estrutura da tabela `academic_tasks.xs`.
   - *Alternativa considerada*: Criar uma tabela separada `activity_grades`. Como a relação entre uma atividade do aluno e a sua nota correspondente é 1:1, a inclusão direta na tabela existente simplifica o modelo de dados, evita joins adicionais e mantém consistência com os endpoints existentes de tarefas.

2. **Suporte no endpoint PATCH de tarefas**:
   - *Decisão*: Incluir `decimal grade?` no bloco `input` e no dicionário `data` de `api/academic_tasks/academic_tasks_id_PATCH.xs`.
   - *Alternativa considerada*: Criar um endpoint exclusivo `POST /academic_tasks/{id}/grade`. O uso do `PATCH` existente respeita o padrão RESTful já adotado no projeto e reduz fragmentação de código.

3. **Experiência de Uso no Frontend Streamlit**:
   - *Decisão*: Na visualização de cada tarefa em `pages/2_📝_Tarefas.py`, quando o status for "Concluído", exibir a nota atribuída (`Nota: X.X / 10.0`) e permitir sua atualização rápida ou via formulário detalhado com `st.number_input` (intervalo de 0.0 a 10.0, passo 0.1).
   - *Alternativa considerada*: Exigir a nota antes de marcar como concluída. A flexibilidade de marcar como concluída e lançar a nota posteriormente atende ao fluxo real de alunos que entregam a tarefa e aguardam a correção.

## Risks / Trade-offs

- **[Risco]** Tarefas já existentes sem o campo `grade` preenchido.
  - *Mitigação*: O campo no schema é opcional (`decimal grade?`), e o frontend trata valores nulos exibindo "Sem nota registrada" sem quebras de execução.
- **[Risco]** Entrada de notas com formato inválido.
  - *Mitigação*: `st.number_input` no Streamlit valida os limites numéricos (mínimo 0.0 e máximo 10.0) diretamente no cliente antes da requisição à API.
