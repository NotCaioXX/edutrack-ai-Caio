# Design: Média de Notas na Página de Progresso e no Relatório PDF

## Context

O EduTrack AI possui suporte ao cadastro de notas em tarefas concluídas (`grade` em `academic_tasks`). A página de progresso (`pages/3_📊_Progresso.py`) consome a lógica em `scripts/calculate_progress.py`, que por sua vez alimenta tanto a interface Streamlit quanto o gerador de PDF `scripts/generate_pdf_report.py`. Atualmente, ambas as saídas apenas exibem contagens e percentuais de conclusão.

## Goals / Non-Goals

**Goals:**
- Estender `calculate_progress_metrics` em `scripts/calculate_progress.py` para calcular `average_grade` (média das notas das tarefas que possuem nota válida) e `graded_tasks`.
- Exibir a média geral no Resumo Executivo e a média de cada matéria na visualização detalhada em `pages/3_📊_Progresso.py`.
- Integrar a média de notas no resumo e na tabela detalhada do relatório em PDF gerado por `scripts/generate_pdf_report.py`.
- Manter o padrão visual sem emojis e adaptado ao tema escuro.

**Non-Goals:**
- Não criar ponderação por peso de tarefas (calcular média aritmética simples das notas registradas).
- Não alterar schemas no Xano (o campo `grade` já existe).

## Decisions

1. **Cálculo da Média em `scripts/calculate_progress.py`**:
   - Considerar apenas tarefas cujo `grade` não seja nulo e seja numérico (`isinstance(t.get("grade"), (int, float))`).
   - Retornar `average_grade` (float ou `None` se nenhuma tarefa avaliada) e `graded_tasks` (int).
2. **Exibição na Página de Progresso**:
   - No Resumo Executivo: 5 colunas de métricas (`Disciplinas Ativas`, `Total de Tarefas`, `Tarefas Concluídas`, `Média Geral`, `Progresso Geral`).
   - No Detalhamento por Disciplina: incluir métrica `Média de Notas: X.X / 10.0` (ou "Sem notas").
3. **Inclusão no Relatório PDF (`generate_pdf_report.py`)**:
   - No Resumo Executivo do PDF: adicionar card de "Média Geral".
   - Na tabela de disciplinas: adicionar coluna "Média" ao lado de "Progresso".

## Risks / Trade-offs

- **[Risco]** Disciplinas ou alunos sem nenhuma nota cadastrada ainda.
  - *Mitigação*: Tratar `average_grade == None` exibindo `-` no PDF e `Sem notas` no Streamlit, sem falha de execução.
